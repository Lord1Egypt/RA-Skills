'use strict';

const BOOLEAN = new Set([
  'json', 'help', 'version', 'yes', 'flagged', 'unflagged', 'all', 'completed', 'no-due',
]);
const SHORT = { y: 'yes', h: 'help', v: 'version' };
const DUE_FILTERS = new Set(['today', 'overdue', 'upcoming']);
const PRIORITIES = new Set(['none', 'low', 'medium', 'high']);

function invalid(message) {
  return { ok: false, error: { code: 'INVALID_ARGUMENT', message } };
}

/** argv into { command, positional, flags }, or { ok: false, error }. */
function parseArgs(args) {
  const result = { command: null, positional: [], flags: {} };
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (/^-[a-z]$/.test(arg) && SHORT[arg[1]]) {
      result.flags[SHORT[arg[1]]] = true;
      continue;
    }
    if (!arg.startsWith('--')) {
      if (!result.command) result.command = arg;
      else result.positional.push(arg);
      continue;
    }
    const key = arg.slice(2);
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

function pad(n) {
  return String(n).padStart(2, '0');
}

/** Local "YYYY-MM-DD" and "YYYY-MM-DDTHH:mm" for a Date. */
function localStamp(date) {
  const day = `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`;
  return { day, minute: `${day}T${pad(date.getHours())}:${pad(date.getMinutes())}` };
}

/**
 * A due date as typed into { date, time } in local time. Takes YYYY-MM-DD,
 * YYYY-MM-DD HH:mm (or with a T), and today / tomorrow with an optional HH:mm.
 */
function parseDue(raw, now = new Date()) {
  const text = String(raw).trim().toLowerCase();
  let m = /^(today|tomorrow)(?:[ t]+(\d{1,2}):(\d{2}))?$/.exec(text);
  if (m) {
    const d = new Date(now.getFullYear(), now.getMonth(), now.getDate() + (m[1] === 'tomorrow' ? 1 : 0));
    return withTime(localStamp(d).day, m[2], m[3], raw);
  }
  m = /^(\d{4})-(\d{2})-(\d{2})(?:[ t](\d{1,2}):(\d{2}))?$/.exec(text);
  if (!m) throw new Error(`--due wants YYYY-MM-DD, "YYYY-MM-DD HH:mm", today or tomorrow, got: ${raw}`);
  const d = new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3]));
  if (d.getMonth() !== Number(m[2]) - 1 || d.getDate() !== Number(m[3])) throw new Error(`not a date: ${raw}`);
  return withTime(`${m[1]}-${m[2]}-${m[3]}`, m[4], m[5], raw);
}

function withTime(date, h, min, raw) {
  if (h === undefined) return { date, time: null };
  if (Number(h) > 23 || Number(min) > 59) throw new Error(`not a time: ${raw}`);
  return { date, time: `${pad(h)}:${min}` };
}

/** A reminder's due string against now: "overdue", "today", "upcoming" or null. */
function dueBucket(due, now = new Date()) {
  if (!due) return null;
  const { day, minute } = localStamp(now);
  const timed = due.includes('T');
  if (timed ? due < minute : due.slice(0, 10) < day) return 'overdue';
  if (due.slice(0, 10) === day) return 'today';
  return 'upcoming';
}

/** Flags into the change set the JXA scripts apply, or throws on a bad value. */
function toChanges(flags, now) {
  const ch = {};
  if (flags.title !== undefined) ch.title = flags.title;
  if (flags.notes !== undefined) ch.notes = flags.notes;
  if (flags.url !== undefined) ch.url = flags.url;
  if (flags.priority !== undefined) {
    const p = String(flags.priority).toLowerCase();
    if (!PRIORITIES.has(p)) throw new Error(`--priority wants none, low, medium or high, got: ${flags.priority}`);
    ch.priority = p;
  }
  if (flags.due !== undefined && flags['no-due']) throw new Error('--due and --no-due together');
  if (flags.due !== undefined) ch.due = parseDue(flags.due, now);
  if (flags['no-due']) ch.due = null;
  return ch;
}

/** Due filter, sort (soonest first, undated last) and limit for a fetched list. */
function select(reminders, { due, limit } = {}, now = new Date()) {
  let out = reminders;
  if (due) {
    if (!DUE_FILTERS.has(due)) throw new Error(`--due wants today, overdue or upcoming, got: ${due}`);
    out = out.filter((r) => {
      const b = dueBucket(r.due, now);
      // Today in Reminders.app also shows what is overdue.
      return due === 'today' ? b === 'today' || b === 'overdue' : b === due;
    });
  }
  out = [...out].sort((a, b) => {
    if (a.due !== b.due) return !a.due ? 1 : !b.due ? -1 : a.due < b.due ? -1 : 1;
    return a.title.localeCompare(b.title);
  });
  return limit ? out.slice(0, limit) : out;
}

function dueText(due) {
  return due ? due.replace('T', ' ') : '';
}

function formatReminder(r) {
  const lines = [`${r.completed ? '[x]' : '[ ]'} ${r.title}`];
  lines.push(`  List: ${r.list}`);
  if (r.due) lines.push(`  Due: ${dueText(r.due)}`);
  if (r.priority !== 'none') lines.push(`  Priority: ${r.priority}`);
  if (r.flagged) lines.push('  Flagged');
  if (r.notes) lines.push(`  Notes: ${r.notes.replace(/\n/g, '\n         ')}`);
  if (r.url) lines.push(`  URL: ${r.url}`);
  if (r.completedAt) lines.push(`  Completed: ${r.completedAt}`);
  lines.push(`  ID: ${r.id}`);
  return lines.join('\n');
}

function formatRow(r) {
  const marks = [r.priority !== 'none' && `!${r.priority}`, r.flagged && 'flagged'].filter(Boolean).join(' ');
  const due = r.due ? `  (due ${dueText(r.due)})` : '';
  return `${r.completed ? '[x]' : '[ ]'} ${r.title}${due}${marks ? `  ${marks}` : ''}\n    ${r.list} | ${r.id}`;
}

function formatReminders(list) {
  return list.length ? list.map(formatRow).join('\n') : 'No reminders.';
}

function formatLists(lists) {
  if (!lists.length) return 'No lists.';
  return lists
    .map((l) => `${l.name}  (${l.open} open${l.writable ? '' : ', read only'})\n    ${l.source} | ${l.id}`)
    .join('\n');
}

module.exports = {
  parseArgs,
  parseDue,
  dueBucket,
  toChanges,
  select,
  formatReminder,
  formatReminders,
  formatLists,
};
