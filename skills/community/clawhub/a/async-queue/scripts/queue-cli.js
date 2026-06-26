#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');

const QUEUE_PATH = path.join(__dirname, 'queue.json');
const HISTORY_PATH = path.join(__dirname, 'history.json');

function loadJson(filePath) {
  try {
    const raw = fs.readFileSync(filePath, 'utf8');
    const data = JSON.parse(raw);
    return Array.isArray(data) ? data : [];
  } catch (_) {
    return [];
  }
}

function saveJson(filePath, data) {
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
}

function padRight(str, len) {
  const s = String(str || '');
  if (s.length >= len) return s;
  return s + ' '.repeat(len - s.length);
}

function truncate(str, len) {
  const s = String(str || '');
  if (s.length <= len) return s;
  if (len <= 3) return s.slice(0, len);
  return s.slice(0, len - 3) + '...';
}

function formatRunAt(iso) {
  const d = new Date(iso);
  if (isNaN(d)) return String(iso || '');
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, '0');
  const dd = String(d.getDate()).padStart(2, '0');
  const hh = String(d.getHours()).padStart(2, '0');
  const min = String(d.getMinutes()).padStart(2, '0');
  return `${yyyy}-${mm}-${dd} ${hh}:${min}`;
}

function printTable(rows, widths) {
  const header = [
    padRight('ID', widths.id),
    padRight('TO', widths.to),
    padRight('TASK', widths.task),
    padRight('FIRES-AT', widths.fires),
  ].join('  ');

  const separator = [
    '-'.repeat(widths.id),
    '-'.repeat(widths.to),
    '-'.repeat(widths.task),
    '-'.repeat(widths.fires),
  ].join('  ');

  console.log(header);
  console.log(separator);
  for (const row of rows) {
    console.log([
      padRight(row.id, widths.id),
      padRight(row.to, widths.to),
      padRight(row.task, widths.task),
      padRight(row.fires, widths.fires),
    ].join('  '));
  }
}

function printHistoryTable(rows, widths) {
  const header = [
    padRight('ID', widths.id),
    padRight('TO', widths.to),
    padRight('STATUS', widths.status),
    padRight('FIRED-AT', widths.fired),
    padRight('TASK', widths.task),
  ].join('  ');

  const separator = [
    '-'.repeat(widths.id),
    '-'.repeat(widths.to),
    '-'.repeat(widths.status),
    '-'.repeat(widths.fired),
    '-'.repeat(widths.task),
  ].join('  ');

  console.log(header);
  console.log(separator);
  for (const row of rows) {
    console.log([
      padRight(row.id, widths.id),
      padRight(row.to, widths.to),
      padRight(row.status, widths.status),
      padRight(row.fired, widths.fired),
      padRight(row.task, widths.task),
    ].join('  '));
  }
}

function cmdList() {
  const queue = loadJson(QUEUE_PATH).slice().sort((a, b) => {
    const ra = Date.parse(a.runAt || '');
    const rb = Date.parse(b.runAt || '');
    return (isNaN(ra) ? 0 : ra) - (isNaN(rb) ? 0 : rb);
  });

  if (queue.length === 0) {
    console.log('No pending tasks.');
    return;
  }

  const rows = queue.map((item) => ({
    id: truncate(String(item.id || '').slice(0, 8), 8),
    to: truncate(item.to || '', 10),
    task: truncate(item.task || '', 60),
    fires: truncate(formatRunAt(item.runAt), 20),
  }));

  printTable(rows, { id: 8, to: 10, task: 60, fires: 20 });
}

function cmdCancel(prefix) {
  if (!prefix) {
    console.error('Usage: node queue/queue-cli.js cancel <idPrefix>');
    process.exit(1);
  }
  const queue = loadJson(QUEUE_PATH);
  const matches = queue.filter((item) => String(item.id || '').startsWith(prefix));
  if (matches.length === 0) {
    console.error(`No tasks found with id prefix: ${prefix}`);
    process.exit(1);
  }
  if (matches.length > 1) {
    const ids = matches.map((m) => String(m.id || '').slice(0, 8)).join(', ');
    console.error(`Multiple matches: ${ids}`);
    process.exit(1);
  }
  const target = matches[0];
  const remaining = queue.filter((item) => item !== target);
  saveJson(QUEUE_PATH, remaining);
  console.log(`Cancelled ${target.id}: ${target.task}`);
}

function cmdHistory() {
  const history = loadJson(HISTORY_PATH);
  if (history.length === 0) {
    console.log('No history entries.');
    return;
  }

  const tail = history.slice(-20);
  const rows = tail.map((item) => ({
    id: truncate(String(item.id || '').slice(0, 8), 8),
    to: truncate(item.to || '', 10),
    status: truncate(item.status || '', 8),
    fired: truncate(formatRunAt(item.firedAt || item.runAt), 20),
    task: truncate(item.task || '', 60),
  }));

  printHistoryTable(rows, { id: 8, to: 10, status: 8, fired: 20, task: 60 });
}

function usage() {
  console.log('Usage: node queue/queue-cli.js <list|cancel|history> [idPrefix]');
}

const cmd = process.argv[2];
if (cmd === 'list') {
  cmdList();
} else if (cmd === 'cancel') {
  cmdCancel(process.argv[3]);
} else if (cmd === 'history') {
  cmdHistory();
} else {
  usage();
  process.exit(1);
}
