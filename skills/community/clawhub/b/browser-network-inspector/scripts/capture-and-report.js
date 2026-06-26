#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

function usage() {
  console.error('Usage: node capture-and-report.js [--base-dir reports/browser-network-inspector] [--include-hosts a,b] [--exclude-hosts a,b] [--no-websocket] [--open-report] [--label name]');
  process.exit(1);
}

const args = process.argv.slice(2);
function getFlag(name) {
  const idx = args.indexOf(name);
  if (idx === -1) return null;
  return args[idx + 1] ?? null;
}
function hasFlag(name) {
  return args.includes(name);
}

if (hasFlag('--help')) usage();

const workspace = path.join(process.env.USERPROFILE || process.env.HOME || '.', '.openclaw', 'workspace');
const skillDir = path.join(workspace, 'skills', 'browser-network-inspector');
const captureScript = path.join(skillDir, 'scripts', 'capture-session.js');

const baseDirArg = getFlag('--base-dir') || 'reports/browser-network-inspector';
const baseDir = path.isAbsolute(baseDirArg) ? baseDirArg : path.join(workspace, baseDirArg);
const includeHosts = getFlag('--include-hosts') || '';
const excludeHosts = getFlag('--exclude-hosts') || '';
const noWebSocket = hasFlag('--no-websocket');
const openReport = hasFlag('--open-report');
const label = (getFlag('--label') || 'capture').replace(/[^a-zA-Z0-9-_]+/g, '-');

function stamp() {
  const d = new Date();
  const p = n => String(n).padStart(2, '0');
  return `${d.getFullYear()}${p(d.getMonth() + 1)}${p(d.getDate())}-${p(d.getHours())}${p(d.getMinutes())}${p(d.getSeconds())}`;
}

const outDir = path.join(baseDir, `${stamp()}-${label}`);
fs.mkdirSync(outDir, { recursive: true });
const jsonOut = path.join(outDir, 'session.json');
const mdOut = path.join(outDir, 'session.md');

const cmd = [
  process.execPath,
  captureScript,
  '--json-out', jsonOut,
  '--md-out', mdOut,
];
if (includeHosts) cmd.push('--include-hosts', includeHosts);
if (excludeHosts) cmd.push('--exclude-hosts', excludeHosts);
if (noWebSocket) cmd.push('--no-websocket');

execFileSync(cmd[0], cmd.slice(1), {
  cwd: workspace,
  encoding: 'utf8',
  stdio: ['ignore', 'inherit', 'inherit'],
  maxBuffer: 20 * 1024 * 1024,
});

if (openReport) {
  execFileSync('cmd.exe', ['/c', 'start', '', mdOut], {
    cwd: workspace,
    windowsHide: true,
    stdio: ['ignore', 'ignore', 'ignore'],
  });
}

console.log(`Report directory: ${outDir}`);
console.log(`JSON: ${jsonOut}`);
console.log(`Markdown: ${mdOut}`);
