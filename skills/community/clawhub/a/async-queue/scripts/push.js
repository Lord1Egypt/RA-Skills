#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const { randomUUID } = require('crypto');

const argv = process.argv.slice(2);
const args = {};
for (let i = 0; i < argv.length; i++) {
  const a = argv[i];
  if (a === '--to' || a === '--task' || a === '--delay' || a === '--then') {
    args[a.slice(2)] = argv[i + 1];
    i++;
  }
}

const now = new Date();

const configPath = path.join(__dirname, 'config.json');
let defaultTo = 'marcus';
try {
  const raw = fs.readFileSync(configPath, 'utf8');
  const cfg = JSON.parse(raw);
  if (cfg && typeof cfg.defaultTo === 'string' && cfg.defaultTo.trim()) {
    defaultTo = cfg.defaultTo.trim();
  }
} catch (_) {}

if (!args.to) args.to = defaultTo;

if (!args.task || !args.delay) {
  console.error('Usage: node push.js --task "text" --delay 20m [--to agent] [--then "next task"]');
  process.exit(1);
}

function nextTime(now, hours, minutes) {
  const runAt = new Date(now);
  runAt.setHours(hours, minutes, 0, 0);
  if (runAt.getTime() <= now.getTime()) {
    runAt.setDate(runAt.getDate() + 1);
  }
  return runAt;
}

function parseDelay(str, now) {
  const s = String(str || '').trim();
  let m = /^([0-9]+)\s*([smh])$/i.exec(s);
  if (m) {
    const n = parseInt(m[1], 10);
    const unit = m[2].toLowerCase();
    const ms = unit === 's' ? n * 1000 : unit === 'm' ? n * 60 * 1000 : n * 60 * 60 * 1000;
    return new Date(now.getTime() + ms);
  }

  m = /^([01]?\d|2[0-3]):([0-5]\d)$/.exec(s);
  if (m) {
    const hours = parseInt(m[1], 10);
    const minutes = parseInt(m[2], 10);
    return nextTime(now, hours, minutes);
  }

  m = /^([1-9]|1[0-2]):([0-5]\d)\s*(am|pm)$/i.exec(s);
  if (m) {
    let hours = parseInt(m[1], 10);
    const minutes = parseInt(m[2], 10);
    const meridiem = m[3].toLowerCase();
    if (meridiem === 'pm' && hours !== 12) hours += 12;
    if (meridiem === 'am' && hours === 12) hours = 0;
    return nextTime(now, hours, minutes);
  }

  return null;
}

const runAt = parseDelay(args.delay, now);
if (!runAt) {
  console.error('Invalid delay. Use 10s, 5m, 2h, HH:MM, or H:MMam/pm.');
  process.exit(1);
}

const item = {
  id: randomUUID(),
  to: args.to,
  task: args.task,
  runAt: runAt.toISOString(),
  createdAt: now.toISOString(),
  ttl: 300,
};
if (args.then) item.then = args.then;

const queuePath = path.join(__dirname, 'queue.json');
let queue = [];
try {
  const raw = fs.readFileSync(queuePath, 'utf8');
  queue = JSON.parse(raw);
  if (!Array.isArray(queue)) queue = [];
} catch (_) {
  queue = [];
}

queue.push(item);
fs.writeFileSync(queuePath, JSON.stringify(queue, null, 2));

const hh = String(runAt.getHours()).padStart(2, '0');
const mm = String(runAt.getMinutes()).padStart(2, '0');
console.log(`Queued ${item.id}: ${item.task} fires at ${hh}:${mm}`);
