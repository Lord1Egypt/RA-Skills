#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { execFileSync, spawnSync } = require('child_process');

const workspace = path.join(process.env.USERPROFILE || process.env.HOME || '.', '.openclaw', 'workspace');

function resolveAgentBrowser() {
  const candidates = [
    path.join(process.env.USERPROFILE || '', '.nvm', 'nodejs', 'node_modules', 'agent-browser', 'bin', 'agent-browser-win32-x64.exe'),
    path.join(process.env.APPDATA || '', 'npm', 'agent-browser.cmd'),
    path.join(process.env.APPDATA || '', 'npm', 'agent-browser'),
    path.join(process.env.USERPROFILE || '', '.nvm', 'nodejs', 'agent-browser.cmd'),
    path.join(process.env.USERPROFILE || '', '.nvm', 'nodejs', 'agent-browser'),
  ].filter(Boolean);

  for (const candidate of candidates) {
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
const out = execFileSync(agentBrowserBin, ['eval', 'window.__bniClear ? window.__bniClear() : false'], {
  cwd: workspace,
  encoding: 'utf8',
  stdio: ['ignore', 'pipe', 'pipe'],
  maxBuffer: 10 * 1024 * 1024,
  shell: false,
  windowsHide: true,
});
console.log(String(out).trim() || 'cleared');
