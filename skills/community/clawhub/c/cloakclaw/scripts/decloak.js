#!/usr/bin/env node
/**
 * CloakClaw skill wrapper — decloak an LLM response.
 * Usage: node decloak.js --session <sessionId> --input <file_or_text>
 * Output: decloaked text to stdout
 * Requires: cloakclaw installed globally (npm install -g cloakclaw)
 */

import { execFileSync } from 'child_process';
import { existsSync, writeFileSync, unlinkSync, mkdtempSync } from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';

const args = process.argv.slice(2);
const getArg = (name) => { const i = args.indexOf(`--${name}`); return i >= 0 ? args[i + 1] : null; };

const sessionId = getArg('session');
const input = getArg('input');

if (!sessionId || !input) {
  console.error('Usage: node decloak.js --session <sessionId> --input <file_or_text>');
  process.exit(1);
}

let tmpFile = null;

try {
  const cliArgs = ['decloak', '-s', sessionId];

  if (existsSync(input)) {
    cliArgs.push('-f', input);
  } else {
    // Raw text — write to temp file
    const tmp = mkdtempSync(join(tmpdir(), 'cloakclaw-'));
    tmpFile = join(tmp, 'response.txt');
    writeFileSync(tmpFile, input, 'utf-8');
    cliArgs.push('-f', tmpFile);
  }

  const result = execFileSync('cloakclaw', cliArgs, {
    encoding: 'utf-8',
    timeout: 60_000,
    maxBuffer: 10 * 1024 * 1024,
  });

  console.log(result);
} catch (e) {
  const msg = e.stderr ? e.stderr.trim() : e.message;
  console.error(msg);
  process.exit(1);
} finally {
  if (tmpFile) try { unlinkSync(tmpFile); } catch {}
}
