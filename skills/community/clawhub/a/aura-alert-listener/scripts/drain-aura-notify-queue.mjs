#!/usr/bin/env node
import fs from 'node:fs';

const QUEUE_FILE = process.env.AURA_NOTIFY_QUEUE_FILE || './memory/aura-notify-queue.jsonl';
const MAX_ITEMS = Number(process.env.AURA_NOTIFY_MAX_ITEMS || 10);

if (!fs.existsSync(QUEUE_FILE)) process.exit(0);

const raw = fs.readFileSync(QUEUE_FILE, 'utf8');
if (!raw.trim()) process.exit(0);

const rows = raw
  .split('\n')
  .map((l) => l.trim())
  .filter(Boolean)
  .map((l) => {
    try { return JSON.parse(l); } catch { return null; }
  })
  .filter(Boolean);

if (!rows.length) {
  fs.writeFileSync(QUEUE_FILE, '');
  process.exit(0);
}

const take = rows.slice(0, MAX_ITEMS);
const rest = rows.slice(MAX_ITEMS);
fs.writeFileSync(QUEUE_FILE, rest.map((r) => JSON.stringify(r)).join('\n') + (rest.length ? '\n' : ''));

const lines = take.map((a) => {
  const id = a?.data?.job_id || a?.data?.task_id || a?.data?.push_alert_id || '';
  const idText = id ? ` (${id})` : '';
  return `- [${a.priority || 'info'}] ${a.type}${idText}: ${a.message || ''}`;
});

const msg = `Aura updates (${take.length})\n${lines.join('\n')}`;
process.stdout.write(msg);
