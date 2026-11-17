#!/usr/bin/env node
'use strict';

const readline = require('readline');
const { runScript, EXIT_VALIDATION_ERROR } = require('../lib/jxa-runner');
const { parseArgs, toChanges, select, formatReminder, formatReminders, formatLists } = require('../lib/cli');
const { version } = require('../package.json');

const HELP = `arcli: Apple Reminders CLI for macOS

USAGE:
  arcli <command> [options]

COMMANDS:
  setup                   Trigger the macOS Reminders permission
  lists                   Every reminder list, with its open count
  reminders [list]        Reminders, open ones by default, from one list or all
  show <id>               One reminder
  add <title>             Add a reminder
  edit <id>               Change a reminder
  complete <id>           Mark done
  uncomplete <id>         Mark not done
  delete <id>             Remove a reminder (asks first; -y to skip)

LISTING (reminders):
  --list-id <id>          Pick the list by id instead of name
  --due <when>            today (includes overdue), overdue or upcoming
  --all                   Include completed reminders
  --completed             Only completed reminders
  --flagged               Only flagged reminders
  --limit <n>             At most n results

FIELDS (add and edit):
  --title <text>          New title (edit)
  --list <name>           List to add to, or move to (--list-id <id> also works)
  --due <when>            YYYY-MM-DD, "YYYY-MM-DD HH:mm", today, tomorrow, "tomorrow 09:00"
  --no-due                Clear the due date (edit)
  --notes <text>          Notes
  --url <url>             URL
  --priority <p>          none, low, medium or high
  --flagged / --unflagged Set or clear the flag

GLOBAL OPTIONS:
  --json       Output JSON (errors included as JSON)
  -h, --help   Show help
  --version    Print version

EXAMPLES:
  arcli reminders Groceries --json
  arcli reminders --due today
  arcli add "Buy milk" --list Groceries --due "tomorrow 09:00" --priority high
  arcli complete <id>`;

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

async function call(script, args, json) {
  const res = await runScript(script, args);
  if (!res.success) fail(json, res.error, res.exitCode);
  return res.data;
}

async function run(script, args, json, human) {
  emit(json, await call(script, args, json), human);
}

async function main() {
  const parsed = parseArgs(process.argv.slice(2));
  if (!parsed.ok) fail(process.argv.includes('--json'), parsed.error, EXIT_VALIDATION_ERROR);
  const { command, positional, flags } = parsed.result;
  const json = Boolean(flags.json);

  if (flags.version) return write(1, version);
  if (flags.help || !command) return write(1, HELP);

  const need = (what) =>
    fail(json, { code: 'MISSING_REQUIRED', message: `${command} needs ${what}` }, EXIT_VALIDATION_ERROR);
  const bad = (err) => fail(json, { code: 'INVALID_ARGUMENT', message: err.message }, EXIT_VALIDATION_ERROR);
  const changes = () => {
    try {
      return toChanges(flags);
    } catch (err) {
      return bad(err);
    }
  };
  if (flags.flagged && flags.unflagged) return bad(new Error('--flagged and --unflagged together'));
  const shown = (verb) => (d) => `${verb}:\n\n${formatReminder(d.reminder)}`;

  switch (command) {
    case 'setup':
      return run('setup', {}, json, (d) => `${d.message}: ${d.lists} list(s) visible`);
    case 'lists':
      return run('lists', {}, json, (d) => formatLists(d.lists));
    case 'reminders': {
      if (flags.all && flags.completed) return bad(new Error('--all and --completed together'));
      const limit = flags.limit === undefined ? undefined : Number(flags.limit);
      if (limit !== undefined && !(Number.isInteger(limit) && limit > 0)) return bad(new Error('--limit wants a positive number'));
      const data = await call('reminders', {
        list: positional.join(' ') || undefined,
        listId: flags['list-id'],
        completed: flags.completed ? 'only' : flags.all ? 'include' : 'exclude',
        flagged: Boolean(flags.flagged),
      }, json);
      let reminders;
      try {
        reminders = select(data.reminders, { due: flags.due, limit });
      } catch (err) {
        return bad(err);
      }
      return emit(json, { ok: true, reminders }, (d) => formatReminders(d.reminders));
    }
    case 'show':
      if (!positional[0]) return need('an id');
      return run('reminder', { id: positional[0] }, json, (d) => formatReminder(d.reminder));
    case 'add': {
      const title = positional.join(' ') || flags.title;
      if (!title) return need('a title');
      const ch = { ...changes(), title };
      return run('add', { list: flags.list, listId: flags['list-id'], changes: ch, flagged: Boolean(flags.flagged) }, json, shown('Added'));
    }
    case 'edit': {
      if (!positional[0]) return need('an id');
      const ch = changes();
      const flagged = flags.flagged ? true : flags.unflagged ? false : undefined;
      if (!Object.keys(ch).length && !flags.list && !flags['list-id'] && flagged === undefined)
        return need('something to change, such as --title, --due, --list or --flagged');
      return run('edit', { id: positional[0], changes: ch, list: flags.list, listId: flags['list-id'], flagged }, json, shown('Updated'));
    }
    case 'complete':
    case 'uncomplete':
      if (!positional[0]) return need('an id');
      return run('edit', { id: positional[0], completed: command === 'complete' }, json, (d) => formatReminder(d.reminder));
    case 'delete': {
      if (!positional[0]) return need('an id');
      if (!flags.yes) {
        if (!process.stdin.isTTY)
          return fail(json, { code: 'MISSING_REQUIRED', message: 'pass -y to delete without a terminal' }, EXIT_VALIDATION_ERROR);
        const found = await call('reminder', { id: positional[0] }, json);
        if (!(await confirm(`Delete "${found.reminder.title}" from ${found.reminder.list}?`))) return;
      }
      return run('delete', { id: positional[0] }, json, (d) => `Deleted "${d.deleted.title}"`);
    }
    default:
      return fail(json, { code: 'INVALID_ARGUMENT', message: `unknown command: ${command}` }, EXIT_VALIDATION_ERROR);
  }
}

main();
