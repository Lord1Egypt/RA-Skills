import fs from 'node:fs';
import { spawnSync } from 'node:child_process';
import process from 'node:process';

import {
  CHROME_CANDIDATES,
  findChromeExecutable,
  getDefaultProfileDir,
} from './xhs-utils.js';

interface CheckResult {
  name: string;
  ok: boolean;
  detail: string;
}

function checkChrome(): CheckResult {
  const chromePath = findChromeExecutable(CHROME_CANDIDATES);
  if (chromePath) {
    return { name: 'Chrome', ok: true, detail: chromePath };
  }
  return {
    name: 'Chrome',
    ok: false,
    detail: 'Not found. Install Chrome or set XHS_BROWSER_CHROME_PATH env var.',
  };
}

function checkProfileDir(): CheckResult {
  const profileDir = getDefaultProfileDir();
  const exists = fs.existsSync(profileDir);
  return {
    name: 'Profile Dir',
    ok: true,
    detail: `${profileDir} (${exists ? 'exists' : 'will be created on first run'})`,
  };
}

function checkBun(): CheckResult {
  const bunResult = spawnSync('bun', ['--version'], { encoding: 'utf-8', timeout: 5000 });
  if (bunResult.status === 0 && bunResult.stdout?.trim()) {
    return { name: 'Bun Runtime', ok: true, detail: `v${bunResult.stdout.trim()}` };
  }

  const npxResult = spawnSync('npx', ['--version'], { encoding: 'utf-8', timeout: 5000 });
  if (npxResult.status === 0 && npxResult.stdout?.trim()) {
    return { name: 'Bun Runtime', ok: true, detail: `npx available (v${npxResult.stdout.trim()}), will use 'npx -y bun'` };
  }

  return {
    name: 'Bun Runtime',
    ok: false,
    detail: 'Neither bun nor npx found. Install bun: npm install -g bun',
  };
}

function checkNodeModules(): CheckResult {
  const scriptDir = new URL('.', import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1');
  const nodeModules = `${scriptDir}/node_modules`;
  const cdpPkg = `${nodeModules}/baoyu-chrome-cdp`;

  if (fs.existsSync(cdpPkg)) {
    return { name: 'Dependencies', ok: true, detail: 'baoyu-chrome-cdp installed' };
  }
  return {
    name: 'Dependencies',
    ok: false,
    detail: 'Missing. Run: cd scripts && npm install',
  };
}

console.log('\n  Xiaohongshu Publisher — Environment Check\n');
console.log('  ─'.repeat(30));

const checks = [checkChrome(), checkProfileDir(), checkBun(), checkNodeModules()];

let allOk = true;
for (const check of checks) {
  const icon = check.ok ? '✓' : '✗';
  const color = check.ok ? '\x1b[32m' : '\x1b[31m';
  console.log(`  ${color}${icon}\x1b[0m ${check.name}: ${check.detail}`);
  if (!check.ok) allOk = false;
}

console.log('\n  ─'.repeat(30));
if (allOk) {
  console.log('  \x1b[32mAll checks passed!\x1b[0m Ready to post to Xiaohongshu.\n');
} else {
  console.log('  \x1b[33mSome checks failed.\x1b[0m Fix the issues above before posting.\n');
  process.exit(1);
}
