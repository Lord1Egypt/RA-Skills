#!/usr/bin/env node
'use strict';

// node:sqlite warns that it is experimental on every run in Node 22; the warning is noise here.
const emitWarning = process.emitWarning;
process.emitWarning = (warning, ...rest) =>
  /SQLite/.test(String(warning)) ? undefined : emitWarning.call(process, warning, ...rest);

const fs = require('fs');
const readline = require('readline');
const { parseArgs, parseSince, formatChats, formatMessages } = require('../lib/cli');
const db = require('../lib/db');
const { sendPlan, runSend } = require('../lib/send');
const { version } = require('../package.json');

const EXIT_RUNTIME_ERROR = 1;
const EXIT_VALIDATION_ERROR = 2;
const EXIT_NOT_AUTHORIZED = 10;

const HELP = `amcli: Apple Messages CLI for macOS

USAGE:
  amcli <command> [options]

COMMANDS:
  chats                   Recent chats, newest first (--unread for only unread)
  show <chat>             Messages in one chat; <chat> is an id, guid, phone or email
  search <text>           Messages containing text, newest first (--chat <chat> to narrow)
  send --to <recipient> [text]
                          Send through Messages.app; text from stdin when omitted.
                          <recipient> is a phone, email or chat guid. Asks first.

OPTIONS:
  --limit <n>             Most results (default 20)
  --since <when>          YYYY-MM-DD, ISO datetime, or 30m, 12h, 7d
  --service sms           send: use SMS instead of iMessage for a phone number
  -y, --yes               send: skip the confirmation
  --dry-run               send: print what would run, send nothing
  --json                  Output JSON (errors included as JSON)
  --help, --version

Reading needs Full Disk Access for your terminal app:
System Settings > Privacy & Security > Full Disk Access.

EXAMPLES:
  amcli chats --unread
  amcli show +15555550123 --limit 50 --since 7d
  amcli search "running late" --json
  echo "Running late" | amcli send --to alex@example.com -y`;

function write(fd, text) {
  const data = Buffer.from(`${text}\n`, 'utf8');
  let written = 0;
  while (written < data.length) {
    try {
      written += fs.writeSync(fd, data, written);
    } catch (err) {
      if (err.code === 'EAGAIN') continue;
      if (err.code === 'EPIPE') return;
      throw err;
    }
  }
}

function emit(json, data, human) {
  write(1, json ? JSON.stringify(data, null, 2) : human(data));
}

function exitCodeFor(code) {
  if (code === 'NOT_AUTHORIZED') return EXIT_NOT_AUTHORIZED;
  if (code === 'INVALID_ARGUMENT' || code === 'MISSING_REQUIRED') return EXIT_VALIDATION_ERROR;
  return EXIT_RUNTIME_ERROR;
}

function fail(json, error) {
  if (json) write(1, JSON.stringify({ ok: false, error }, null, 2));
  else write(2, `Error [${error.code}]: ${error.message}`);
  process.exit(exitCodeFor(error.code));
}

function readStdin() {
  return new Promise((resolve) => {
    let data = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', (d) => (data += d));
    process.stdin.on('end', () => resolve(data));
  });
}

/** Asks on the terminal itself, so it works when stdin carried the message. */
async function confirm(question) {
  const input = process.stdin.isTTY ? process.stdin : fs.createReadStream('/dev/tty');
  const rl = readline.createInterface({ input, output: process.stderr });
  const answer = await new Promise((r) => rl.question(`${question} [y/N] `, r));
  rl.close();
  if (input !== process.stdin) input.destroy();
  return /^y(es)?$/i.test(answer.trim());
}

function options(flags, json) {
  const limit = flags.limit === undefined ? 20 : Number(flags.limit);
  if (!Number.isInteger(limit) || limit < 1)
    fail(json, { code: 'INVALID_ARGUMENT', message: '--limit must be a positive integer' });
  let since = null;
  if (flags.since !== undefined) {
    since = parseSince(flags.since);
    if (!since) fail(json, { code: 'INVALID_ARGUMENT', message: `--since not understood: ${flags.since}` });
  }
  return { limit, since };
}

async function send(flags, positional, json) {
  if (!flags.to) fail(json, { code: 'MISSING_REQUIRED', message: 'send needs --to <phone|email|chat guid>' });
  const service = flags.service || 'imessage';
  if (!/^(imessage|sms)$/i.test(service))
    fail(json, { code: 'INVALID_ARGUMENT', message: '--service is imessage or sms' });
  let text = positional.join(' ');
  if (!text && !process.stdin.isTTY) text = (await readStdin()).replace(/\n+$/, '');
  if (!text.trim()) fail(json, { code: 'MISSING_REQUIRED', message: 'send needs text, as an argument or on stdin' });

  const plan = sendPlan(flags.to, text, service);
  const via = plan.kind === 'chat' ? 'chat' : plan.kind === 'sms' ? 'SMS' : 'iMessage';
  const target = plan.kind === 'chat' ? `chat ${plan.to}` : `${plan.to} via ${via}`;
  if (flags['dry-run']) {
    return emit(json, { dryRun: true, wouldSend: { to: plan.to, via, text, command: ['osascript', ...plan.args] } }, (d) =>
      [`Would send to ${target}:`, text, '', `osascript -e <script> ${JSON.stringify(plan.to)} <text> ${plan.kind}`].join('\n'),
    );
  }
  if (!flags.yes) {
    if (!process.stderr.isTTY || !fs.existsSync('/dev/tty'))
      fail(json, { code: 'MISSING_REQUIRED', message: 'pass --yes to send without a terminal' });
    if (!(await confirm(`Send to ${target}?\n${text}\n`))) {
      write(2, 'Not sent.');
      return;
    }
  }
  try {
    await runSend(plan);
  } catch (err) {
    fail(json, { code: 'SEND_FAILED', message: err.message });
  }
  emit(json, { sent: true, to: plan.to, via }, () => `Sent to ${target}`);
}

async function main() {
  const parsed = parseArgs(process.argv.slice(2));
  if (!parsed.ok) fail(false, parsed.error);
  const { command, positional, flags } = parsed.result;
  const json = Boolean(flags.json);

  if (flags.version) return write(1, version);
  if (flags.help || !command) return write(1, HELP);
  if (command === 'send') return send(flags, positional, json);

  const need = (what) => fail(json, { code: 'MISSING_REQUIRED', message: `${command} needs ${what}` });
  const known = ['chats', 'show', 'search'];
  if (!known.includes(command)) fail(json, { code: 'INVALID_ARGUMENT', message: `unknown command: ${command}` });
  if (command === 'show' && !positional[0]) need('a chat id, guid, phone or email');
  if (command === 'search' && !positional.length) need('text to search for');
  const opts = options(flags, json);

  try {
    const conn = db.open();
    if (command === 'chats') {
      const chats = db.listChats(conn, { limit: opts.limit, unreadOnly: Boolean(flags.unread) });
      return emit(json, { chats }, (d) => formatChats(d.chats));
    }
    if (command === 'show') {
      const chat = db.findChat(conn, positional[0]);
      const messages = db.chatMessages(conn, chat.id, opts);
      return emit(json, { chat, messages }, (d) => `${d.chat.name}\n\n${formatMessages(d.messages)}`);
    }
    const chatId = flags.chat ? db.findChat(conn, flags.chat).id : null;
    const messages = db.searchMessages(conn, positional.join(' '), { ...opts, chatId });
    return emit(json, { messages }, (d) => formatMessages(d.messages, true));
  } catch (err) {
    if (err instanceof db.AmcliError) fail(json, { code: err.code, message: err.message });
    fail(json, { code: 'RUNTIME_ERROR', message: err.message });
  }
}

main();
