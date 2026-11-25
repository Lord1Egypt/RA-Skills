#!/usr/bin/env node
// deadline-radar: parse DEADLINES.md and report what is due.
import fs from 'node:fs';
import { pathToFileURL } from 'node:url';

const LINE = /^\s*-\s*(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})\s*\|\s*([^|]+?)\s*\|\s*(.+?)\s*$/;

function arg(name, fallback) {
  const i = process.argv.indexOf(`--${name}`);
  return i > -1 && process.argv[i + 1] ? process.argv[i + 1] : fallback;
}

// Offset (ms) of an IANA zone at a given instant, from Intl parts.
function zoneOffset(tz, at) {
  const parts = Object.fromEntries(new Intl.DateTimeFormat('en-US', {
    timeZone: tz, hourCycle: 'h23', year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit',
  }).formatToParts(at).map(p => [p.type, p.value]));
  const asUtc = Date.UTC(parts.year, parts.month - 1, parts.day, parts.hour, parts.minute, parts.second);
  return asUtc - at.getTime();
}

export function parseDeadlines(text, tz) {
  const out = [];
  for (const raw of text.split('\n')) {
    const m = LINE.exec(raw);
    if (!m) continue;
    const [, date, time, title, project] = m;
    const naive = new Date(`${date}T${time}:00Z`);
    const due = new Date(naive.getTime() - zoneOffset(tz, naive));
    if (!Number.isNaN(due.getTime())) out.push({ title, project, due });
  }
  return out;
}

export function classifyDeadlines(items, now, days) {
  return items
    .map(d => {
      const hoursLeft = Math.round((d.due - now) / 36e5);
      const urgency = hoursLeft < 0 ? 'overdue' : hoursLeft < 24 ? 'today' : hoursLeft < 72 ? 'soon' : 'upcoming';
      return { title: d.title, project: d.project, due: d.due.toISOString(), hoursLeft, urgency };
    })
    .filter(d => d.hoursLeft < days * 24)
    .sort((a, b) => a.hoursLeft - b.hoursLeft);
}

// Run as a CLI only when this file is the entry point. Compare real paths as
// file URLs so a path with spaces or a symlink (macOS /tmp) still matches.
function isEntryPoint() {
  try {
    return import.meta.url === pathToFileURL(fs.realpathSync(process.argv[1])).href;
  } catch {
    return false;
  }
}

if (isEntryPoint()) {
  const file = arg('file', 'DEADLINES.md');
  const tz = arg('tz', 'America/Los_Angeles');
  const days = Number(arg('days', '7'));
  let text;
  try {
    text = fs.readFileSync(file, 'utf8');
  } catch {
    console.error(`deadline-radar: cannot read ${file}`);
    process.exit(2);
  }
  const result = classifyDeadlines(parseDeadlines(text, tz), new Date(), days);
  if (process.argv.includes('--json')) {
    console.log(JSON.stringify(result, null, 2));
  } else if (!result.length) {
    console.log(`Nothing due in the next ${days} days.`);
  } else {
    for (const d of result) console.log(`${d.urgency.padEnd(8)} ${String(d.hoursLeft).padStart(5)}h  ${d.title} (${d.project})`);
  }
}
