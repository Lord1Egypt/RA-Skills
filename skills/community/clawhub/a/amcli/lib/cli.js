'use strict';

const BOOLEAN = new Set(['json', 'help', 'version', 'yes', 'unread', 'dry-run']);
const SHORT = { y: 'yes', h: 'help' };

/** argv into { command, positional, flags }, or { ok: false, error }. */
function parseArgs(args) {
  const result = { command: null, positional: [], flags: {} };
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    let key = null;
    if (arg.startsWith('--') && arg.length > 2) key = arg.slice(2);
    else if (/^-[a-z]$/.test(arg) && SHORT[arg[1]]) key = SHORT[arg[1]];
    if (!key) {
      if (!result.command) result.command = arg;
      else result.positional.push(arg);
      continue;
    }
    if (BOOLEAN.has(key)) {
      result.flags[key] = true;
      continue;
    }
    const value = args[i + 1];
    if (value === undefined || value.startsWith('--')) {
      return { ok: false, error: { code: 'MISSING_REQUIRED', message: `--${key} requires a value` } };
    }
    i++;
    result.flags[key] = value;
  }
  return { ok: true, result };
}

/** `--since` as YYYY-MM-DD, an ISO datetime, or relative: 30m, 12h, 7d. */
function parseSince(raw, now = new Date()) {
  const rel = /^(\d+)([mhd])$/.exec(raw);
  if (rel) {
    const unit = { m: 60e3, h: 3600e3, d: 86400e3 }[rel[2]];
    return new Date(now.getTime() - Number(rel[1]) * unit);
  }
  const d = /^\d{4}-\d{2}-\d{2}$/.test(raw) ? new Date(`${raw}T00:00:00`) : new Date(raw);
  return Number.isNaN(d.getTime()) ? null : d;
}

function localTime(isoString) {
  if (!isoString) return '';
  const d = new Date(isoString);
  const pad = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

function formatChats(chats) {
  if (!chats.length) return 'No chats found.';
  return chats
    .map((c) => {
      const unread = c.unread ? `  (${c.unread} unread)` : '';
      return `${localTime(c.lastMessageAt)}  ${c.name}${unread}\n  id ${c.id}  ${c.service}  ${c.guid}`;
    })
    .join('\n');
}

function formatMessage(m, withChat = false) {
  const who = m.fromMe ? 'me' : m.sender || 'unknown';
  const where = withChat && m.chat ? ` in ${m.chat}` : '';
  const files = m.attachments.length ? `  [${m.attachments.join(', ')}]` : '';
  return `${localTime(m.date)}  ${who}${where} (${m.service || '?'}): ${m.text || ''}${files}`;
}

function formatMessages(messages, withChat = false) {
  if (!messages.length) return 'No messages found.';
  return messages.map((m) => formatMessage(m, withChat)).join('\n');
}

module.exports = { parseArgs, parseSince, localTime, formatChats, formatMessage, formatMessages };
