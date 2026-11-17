#!/usr/bin/env node
'use strict';

const fs = require('fs');
const readline = require('readline');
const { runScript, EXIT_VALIDATION_ERROR } = require('../lib/jxa-runner');
const { parseArgs, htmlToText, textToHtml, noteHtml, formatList, formatFolders, formatNote } = require('../lib/cli');
const { version } = require('../package.json');

const HELP = `ancli: Apple Notes CLI for macOS

USAGE:
  ancli <command> [options]

COMMANDS:
  setup                      Trigger the Automation permission for Notes
  folders                    Folders with their account and note count
  list                       Notes, most recently modified first
  search <query>             Notes whose title or text contains query
  show <id>                  One note as plain text (--html for the stored HTML)
  create <title> [body]      Add a note; body "-" or piped input reads stdin
  append <id> [text]         Add text to the end of a note; "-" or a pipe reads stdin
  move <id> <folder>         Move a note to another folder
  delete <id>                Delete a note (asks first; -y to skip)

OPTIONS:
  --folder <name|id>  Folder for list, search and create
  --limit <n>         Most notes for list and search (default 20)
  --html              show: print the HTML Notes stores
  -y, --yes           delete: do not ask
  --json              Output JSON (errors included as JSON)
  --help              Show help
  --version           Print version

Ids are the short form shown (p123) or the full x-coredata:// URL.

EXAMPLES:
  ancli list --folder Notes --limit 5
  ancli search "shopping" --json
  ancli create "Shopping list" "Milk" --folder Notes
  echo "Eggs" | ancli append p123`;

function write(fd, text) {
  fs.writeSync(fd, `${text}\n`);
}

function emit(json, data, human) {
  write(1, json ? JSON.stringify(data, null, 2) : human(data));
}

function fail(json, error, code) {
  if (json) write(1, JSON.stringify({ ok: false, error }, null, 2));
  else {
    write(2, `Error [${error.code}]: ${error.message}`);
    for (const c of error.candidates || [])
      write(2, typeof c === 'string' ? `  ${c}` : `  ${c.account}/${c.name}  id ${c.id}`);
  }
  process.exit(code);
}

async function confirm(question) {
  const rl = readline.createInterface({ input: process.stdin, output: process.stderr });
  const answer = await new Promise((r) => rl.question(`${question} [y/N] `, r));
  rl.close();
  return /^y(es)?$/i.test(answer.trim());
}

// Text from the argument, or stdin when it is "-" or something is piped in.
// A terminal or an inherited empty stdin is never read, so nothing hangs.
function textFrom(arg) {
  if (arg !== undefined && arg !== '-') return arg;
  let piped = arg === '-';
  if (!piped) {
    try {
      const st = fs.fstatSync(0);
      piped = st.isFIFO() || st.isFile();
    } catch {
      piped = false;
    }
  }
  return piped ? fs.readFileSync(0, 'utf8') : undefined;
}

async function run(script, args, json, human) {
  const res = await runScript(script, args);
  if (!res.success) fail(json, res.error, res.exitCode);
  emit(json, res.data, human);
}

async function main() {
  const parsed = parseArgs(process.argv.slice(2));
  if (!parsed.ok) fail(process.argv.includes('--json'), parsed.error, EXIT_VALIDATION_ERROR);
  const { command, positional, flags } = parsed.result;
  const json = Boolean(flags.json);

  if (flags.version) return write(1, version);
  if (flags.help || !command) return write(1, HELP);
  if (process.platform !== 'darwin')
    return fail(json, { code: 'UNSUPPORTED', message: 'ancli needs macOS and Notes.app' }, 1);

  const need = (what) =>
    fail(json, { code: 'MISSING_REQUIRED', message: `${command} needs ${what}` }, EXIT_VALIDATION_ERROR);
  let limit = 20;
  if (flags.limit !== undefined) {
    limit = Number(flags.limit);
    if (!Number.isInteger(limit) || limit < 1)
      return fail(json, { code: 'INVALID_ARGUMENT', message: '--limit must be a positive whole number' }, EXIT_VALIDATION_ERROR);
  }

  switch (command) {
    case 'setup':
      return run('setup', {}, json, (d) => `${d.message}: ${d.count} note(s) in ${d.accounts.join(', ')}`);
    case 'folders':
      return run('folders', {}, json, formatFolders);
    case 'list':
      return run('list', { folder: flags.folder, limit }, json, formatList);
    case 'search':
      if (!positional.length) return need('a query');
      return run('search', { query: positional.join(' '), folder: flags.folder, limit }, json, formatList);
    case 'show': {
      if (!positional[0]) return need('an id');
      const res = await runScript('show', { id: positional[0] });
      if (!res.success) fail(json, res.error, res.exitCode);
      const note = res.data.note;
      if (json && !flags.html && note.body !== null) note.text = htmlToText(note.body);
      if (json && !flags.html) delete note.body;
      return emit(json, res.data, (d) => formatNote(d.note, flags.html));
    }
    case 'create': {
      const title = positional[0];
      if (!title) return need('a title');
      const body = textFrom(positional.slice(1).join(' ') || undefined);
      return run('create', { html: noteHtml(title, body), folder: flags.folder }, json, (d) =>
        `Created in ${d.note.folder}: ${d.note.title}  id ${d.note.id}`,
      );
    }
    case 'append': {
      if (!positional[0]) return need('an id');
      const text = textFrom(positional.slice(1).join(' ') || undefined);
      if (!text || !text.trim()) return need('text to append');
      return run('append', { id: positional[0], html: textToHtml(text) }, json, (d) =>
        `Appended to ${d.note.title}  id ${d.note.id}`,
      );
    }
    case 'move':
      if (!positional[0] || !positional[1]) return need('an id and a folder');
      return run('move', { id: positional[0], folder: positional.slice(1).join(' ') }, json, (d) =>
        `Moved ${d.note.title} to ${d.note.folder}  id ${d.note.id}`,
      );
    case 'delete': {
      if (!positional[0]) return need('an id');
      if (!flags.yes) {
        if (!process.stdin.isTTY)
          return fail(json, { code: 'MISSING_REQUIRED', message: 'pass --yes to delete without a terminal' }, EXIT_VALIDATION_ERROR);
        const found = await runScript('peek', { id: positional[0] });
        if (!found.success) fail(json, found.error, found.exitCode);
        const n = found.data.note;
        const where = n.folder === 'Recently Deleted' ? 'It is already in Recently Deleted, so this is permanent.' : 'Notes keeps it in Recently Deleted for 30 days.';
        if (!(await confirm(`Delete "${n.title}" from ${n.folder}? ${where}`))) return;
      }
      return run('delete', { id: positional[0] }, json, (d) =>
        d.permanent
          ? `Deleted ${d.deleted.title} for good`
          : `Deleted ${d.deleted.title}; it is in Recently Deleted for 30 days`,
      );
    }
    default:
      fail(json, { code: 'INVALID_ARGUMENT', message: `unknown command: ${command}` }, EXIT_VALIDATION_ERROR);
  }
}

main();
