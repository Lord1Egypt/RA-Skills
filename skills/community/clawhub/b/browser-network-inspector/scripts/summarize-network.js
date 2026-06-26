#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function usage() {
  console.error('Usage: node summarize-network.js <input.json> [output.md]');
  process.exit(1);
}

const inputPath = process.argv[2];
const outputPath = process.argv[3];
if (!inputPath) usage();

const raw = fs.readFileSync(inputPath, 'utf8');
const logs = JSON.parse(raw);
if (!Array.isArray(logs)) throw new Error('Input JSON must be an array');

const total = logs.length;
const failures = logs.filter(x => x.error || (typeof x.status === 'number' && x.status >= 400));
const byMethod = new Map();
const byStatus = new Map();
const byHost = new Map();
const bySource = new Map();

function inc(map, key) { map.set(key, (map.get(key) || 0) + 1); }
function hostOf(url) { try { return new URL(url).host; } catch { return '(invalid-url)'; } }
function topEntries(map, limit = 10) { return [...map.entries()].sort((a, b) => b[1] - a[1]).slice(0, limit); }
function short(v, max = 160) { if (v == null) return ''; const s = typeof v === 'string' ? v : JSON.stringify(v); return s.length > max ? s.slice(0, max) + '…' : s; }

for (const item of logs) {
  inc(byMethod, item.method || 'UNKNOWN');
  inc(bySource, item.source || 'unknown');
  if (typeof item.status === 'number') inc(byStatus, String(item.status));
  inc(byHost, hostOf(item.url || ''));
}

const lines = [];
lines.push('# Browser Network Inspector Report');
lines.push('');
lines.push(`- Total captured events: ${total}`);
lines.push(`- Failed/error events: ${failures.length}`);
lines.push('');

lines.push('## Sources');
for (const [key, value] of topEntries(bySource)) lines.push(`- ${key}: ${value}`);
lines.push('');

lines.push('## Methods');
for (const [key, value] of topEntries(byMethod)) lines.push(`- ${key}: ${value}`);
lines.push('');

lines.push('## Status codes');
for (const [key, value] of topEntries(byStatus)) lines.push(`- ${key}: ${value}`);
lines.push('');

lines.push('## Hosts');
for (const [key, value] of topEntries(byHost)) lines.push(`- ${key}: ${value}`);
lines.push('');

const keyFlows = logs.filter(x => ['fetch','xhr'].includes(x.source)).slice(-20);
lines.push('## Recent HTTP requests');
for (const item of keyFlows) {
  const status = item.error ? `ERROR ${item.error}` : (item.status ?? 'N/A');
  lines.push(`- [${item.source}] ${item.method || 'GET'} ${item.url || ''} -> ${status} (${item.durationMs ?? 'n/a'} ms)`);
}
lines.push('');

const wsEvents = logs.filter(x => x.source === 'websocket').slice(-20);
if (wsEvents.length) {
  lines.push('## Recent WebSocket events');
  for (const item of wsEvents) {
    lines.push(`- [${item.phase || 'event'}] ${item.url || ''} ${item.code ? `code=${item.code}` : ''} ${item.message ? `msg=${short(item.message)}` : ''}`.trim());
  }
  lines.push('');
}

if (failures.length) {
  lines.push('## Failures');
  for (const item of failures.slice(0, 20)) {
    lines.push(`- ${item.method || 'GET'} ${item.url || ''}`);
    if (item.source) lines.push(`  - Source: ${item.source}`);
    if (item.phase) lines.push(`  - Phase: ${item.phase}`);
    if (item.error) lines.push(`  - Error: ${short(item.error)}`);
    if (item.status) lines.push(`  - Status: ${item.status}`);
    if (item.requestBody != null) lines.push(`  - Request body: ${short(item.requestBody)}`);
    if (item.responseBody != null) lines.push(`  - Response body: ${short(item.responseBody)}`);
  }
  lines.push('');
}

const markdown = lines.join('\n');
if (outputPath) {
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, markdown, 'utf8');
} else {
  process.stdout.write(markdown + '\n');
}
