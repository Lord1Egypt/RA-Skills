#!/usr/bin/env node
'use strict';

const readline = require('readline');
const { runScript, EXIT_VALIDATION_ERROR } = require('../lib/jxa-runner');
const { parseArgs, toChanges, formatContact, formatContacts } = require('../lib/cli');
const { version } = require('../package.json');

const HELP = `apcli - Apple Contacts CLI for macOS

USAGE:
  apcli <command> [options]

COMMANDS:
  setup                 Trigger the macOS Contacts permission
  search <query>        Contacts whose name, nickname or company contains query
  contact <id>          One contact by id
  create                Add a contact
  update <id>           Change a contact
  delete <id>           Remove a contact (asks first; --yes to skip)

FIELDS (create and update):
  --given <name>  --family <name>  --nickname <name>  --org <name>
  --phone [label:]<number>         repeatable; label e.g. mobile, home, work
  --email [label:]<address>        repeatable
  --social <service>:<handle>      repeatable; e.g. telegram:@ana, discord:1234...
  --remove-phone <number>  --remove-email <address>  --remove-social <service>:<handle>

GLOBAL OPTIONS:
  --json       Output JSON (errors included as JSON)
  --limit <n>  Most results for search (default 50)
  --help       Show help
  --version    Print version

EXAMPLES:
  apcli search ana --json
  apcli update <id> --social telegram:@ana --social discord:123456789012345678
  apcli create --given Ana --phone mobile:+491701234567`;

function write(fd, text) {
  require('fs').writeSync(fd, `${text}\n`);
}

function emit(json, data, human) {
  write(1, json ? JSON.stringify(data, null, 2) : human(data));
}

function fail(json, error, code) {
  if (json) write(1, JSON.stringify({ ok: false, error }, null, 2));
  else write(2, `Error [${error.code}]: ${error.message}`);
  process.exit(code);
}

async function confirm(question) {
  const rl = readline.createInterface({ input: process.stdin, output: process.stderr });
  const answer = await new Promise((r) => rl.question(`${question} [y/N] `, r));
  rl.close();
  return /^y(es)?$/i.test(answer.trim());
}

async function run(script, args, json, human) {
  const res = await runScript(script, args);
  if (!res.success) fail(json, res.error, res.exitCode);
  emit(json, res.data, human);
}

async function main() {
  const parsed = parseArgs(process.argv.slice(2));
  if (!parsed.ok) fail(false, parsed.error, EXIT_VALIDATION_ERROR);
  const { command, positional, flags, arrays } = parsed.result;
  const json = Boolean(flags.json);

  if (flags.version) return write(1, version);
  if (flags.help || !command) return write(1, HELP);

  const need = (what) =>
    fail(json, { code: 'MISSING_REQUIRED', message: `${command} needs ${what}` }, EXIT_VALIDATION_ERROR);

  switch (command) {
    case 'setup':
      return run('setup', {}, json, (d) => `${d.message}: ${d.count} contact(s) visible`);
    case 'search':
      if (!positional.length) return need('a query');
      return run('search', { query: positional.join(' '), limit: Number(flags.limit) || 50 }, json, (d) =>
        formatContacts(d.contacts),
      );
    case 'contact':
      if (!positional[0]) return need('an id');
      return run('contact', { id: positional[0] }, json, (d) => formatContact(d.contact));
    case 'create': {
      const changes = toChanges(flags, arrays);
      if (!changes.givenName && !changes.familyName && !changes.organization)
        return need('--given, --family or --org');
      return run('create', changes, json, (d) => `Created:\n\n${formatContact(d.contact)}`);
    }
    case 'update':
      if (!positional[0]) return need('an id');
      return run('update', { id: positional[0], changes: toChanges(flags, arrays) }, json, (d) =>
        `Updated:\n\n${formatContact(d.contact)}`,
      );
    case 'delete': {
      if (!positional[0]) return need('an id');
      if (!flags.yes) {
        if (!process.stdin.isTTY)
          return fail(json, { code: 'MISSING_REQUIRED', message: 'pass --yes to delete without a terminal' }, EXIT_VALIDATION_ERROR);
        const found = await runScript('contact', { id: positional[0] });
        if (!found.success) fail(json, found.error, found.exitCode);
        if (!(await confirm(`Delete ${found.data.contact.name}? Contacts keeps no trash.`))) return;
      }
      return run('delete', { id: positional[0] }, json, (d) => `Deleted ${d.deleted.name}`);
    }
    default:
      fail(json, { code: 'INVALID_ARGUMENT', message: `unknown command: ${command}` }, EXIT_VALIDATION_ERROR);
  }
}

main();
