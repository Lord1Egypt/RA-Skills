#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { execFileSync, spawnSync } = require('child_process');

function usage() {
  console.error('Usage: node capture-session.js --json-out <path> [--md-out <path>] [--include-hosts a,b] [--exclude-hosts a,b] [--no-websocket]');
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

const jsonOut = getFlag('--json-out');
const mdOut = getFlag('--md-out');
if (!jsonOut) usage();

const includeHosts = (getFlag('--include-hosts') || '').split(',').map(s => s.trim()).filter(Boolean);
const excludeHosts = (getFlag('--exclude-hosts') || '').split(',').map(s => s.trim()).filter(Boolean);
const captureWebSocket = !hasFlag('--no-websocket');

const workspace = path.join(process.env.USERPROFILE || process.env.HOME || '.', '.openclaw', 'workspace');
const skillDir = path.join(workspace, 'skills', 'browser-network-inspector');
const collectorPath = path.join(skillDir, 'scripts', 'collect-network.js');
const summarizerPath = path.join(skillDir, 'scripts', 'summarize-network.js');

const collector = fs.readFileSync(collectorPath, 'utf8');
const configExpr = `(() => { window.__bniSetConfig(${JSON.stringify({ includeHosts, excludeHosts, captureWebSocket })}); return 'ok'; })()`;

function resolveAgentBrowser() {
  const pathCandidates = [
    path.join(process.env.USERPROFILE || '', '.nvm', 'nodejs', 'node_modules', 'agent-browser', 'bin', 'agent-browser-win32-x64.exe'),
    path.join(process.env.APPDATA || '', 'npm', 'agent-browser.cmd'),
    path.join(process.env.APPDATA || '', 'npm', 'agent-browser'),
    path.join(process.env.USERPROFILE || '', '.nvm', 'nodejs', 'agent-browser.cmd'),
    path.join(process.env.USERPROFILE || '', '.nvm', 'nodejs', 'agent-browser'),
  ].filter(Boolean);

  for (const candidate of pathCandidates) {
    if (candidate && fs.existsSync(candidate)) return candidate;
  }

  const probe = spawnSync('where', ['agent-browser'], { encoding: 'utf8', shell: false });
  if (!probe.error && probe.status === 0 && probe.stdout) {
    const first = probe.stdout.split(/\r?\n/).map(s => s.trim()).filter(Boolean)[0];
    if (first) return first;
  }

  return 'agent-browser';
}

const agentBrowserBin = resolveAgentBrowser();

function runAgentBrowserEval(js) {
  return execFileSync(agentBrowserBin, ['eval', js], {
    cwd: workspace,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    maxBuffer: 20 * 1024 * 1024,
    shell: false,
    windowsHide: true,
  });
}

function injectLargeScript(js) {
  const chunkSize = 6000;
  runAgentBrowserEval('(() => { window.__bniChunkSrc = ""; return "ok"; })()');
  for (let i = 0; i < js.length; i += chunkSize) {
    const chunk = JSON.stringify(js.slice(i, i + chunkSize));
    runAgentBrowserEval(`(() => { window.__bniChunkSrc += ${chunk}; return "ok"; })()`);
  }
  return runAgentBrowserEval('(() => { const out = eval(window.__bniChunkSrc); delete window.__bniChunkSrc; return out; })()');
}

injectLargeScript(collector);
runAgentBrowserEval(configExpr);
const exportedRaw = runAgentBrowserEval("JSON.stringify(window.__bniExport ? window.__bniExport() : [])");
const exported = (() => {
  const trimmed = String(exportedRaw || '').trim();
  const start = trimmed.indexOf('[');
  const end = trimmed.lastIndexOf(']');
  if (start !== -1 && end !== -1 && end >= start) return trimmed.slice(start, end + 1);
  return '[]';
})();

fs.mkdirSync(path.dirname(jsonOut), { recursive: true });
fs.writeFileSync(jsonOut, exported, 'utf8');

if (mdOut) {
  execFileSync(process.execPath, [summarizerPath, jsonOut, mdOut], {
    cwd: workspace,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    maxBuffer: 20 * 1024 * 1024,
  });
}

console.log(`Saved JSON: ${jsonOut}`);
if (mdOut) console.log(`Saved Markdown: ${mdOut}`);
