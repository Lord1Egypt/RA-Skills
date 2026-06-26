#!/usr/bin/env node
/**
 * free-web-search-js environment check v28
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { findBrowserExecutable } from './playwright-support.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const skillRoot = path.resolve(__dirname, '..');

function main() {
  const lines = [];

  // Node.js (use process.versions, no subprocess)
  const v = `v${process.versions.node}`;
  const major = parseInt(process.versions.node.split('.')[0], 10);
  const nodeOk = major >= 18;
  if (nodeOk) {
    lines.push(`[OK] Node.js ${v} (>= 18)`);
  } else {
    lines.push(`[X] Node.js >= 18 required (current: ${v})`);
    lines.push(`   -> https://nodejs.org`);
  }

  // npm dependencies (全部必装)
  const nm = path.join(skillRoot, 'node_modules');
  const requiredDeps = ['cheerio', 'commander', 'iconv-lite', 'playwright'];
  let depsOk = true;

  if (!fs.existsSync(nm)) {
    lines.push(`[X] node_modules not found`);
    lines.push(`   -> cd ${skillRoot} && npm install`);
    depsOk = false;
  } else {
    const missing = requiredDeps.filter(dep => !fs.existsSync(path.join(nm, dep)));
    if (missing.length > 0) {
      lines.push(`[X] Missing npm packages: ${missing.join(', ')}`);
      lines.push(`   -> cd ${skillRoot} && npm install`);
      depsOk = false;
    } else {
      lines.push(`[OK] npm packages: cheerio, commander, iconv-lite, playwright`);
    }
  }

  // Playwright Chromium browser (must include a usable executable, not just a cache folder)
  let browserOk = false;
  try {
    const browserExecutable = findBrowserExecutable();
    browserOk = Boolean(browserExecutable);
    if (browserOk) {
      lines.push(`[OK] Playwright Chromium executable: ${browserExecutable}`);
    } else {
      lines.push(`[X] Playwright Chromium executable not found`);
      lines.push(`   -> cd ${skillRoot} && bash scripts/setup.sh`);
      lines.push(`   -> or: npx playwright install chromium`);
      lines.push(`   -> optional: set CHROMIUM_EXECUTABLE_PATH=/path/to/chrome`);
      depsOk = false;
    }
  } catch (e) {
    lines.push(`[X] Playwright Chromium browser check failed: ${e.message}`);
    lines.push(`   -> npx playwright install chromium`);
    depsOk = false;
  }

  const allOk = nodeOk && depsOk;
  lines.push('');
  if (allOk) {
    lines.push(`[OK] Environment ready`);
  } else {
    lines.push(`[X] Environment not ready, follow the -> hints above`);
  }

  console.log(lines.join('\n'));
  process.exit(allOk ? 0 : 1);
}

main();
