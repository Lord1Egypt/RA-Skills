#!/usr/bin/env node
/**
 * CloakClaw skill wrapper — cloak a document or text.
 * Usage: node cloak.js --profile <profile> --input <file_or_text> [--no-llm]
 * Output: cloaked text to stdout (session ID printed to stderr by cloakclaw)
 * Requires: cloakclaw installed globally (npm install -g cloakclaw)
 */

import { execFileSync, execSync } from 'child_process';
import { existsSync, writeFileSync, unlinkSync, mkdtempSync } from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';

const args = process.argv.slice(2);
const getArg = (name) => { const i = args.indexOf(`--${name}`); return i >= 0 ? args[i + 1] : null; };
const hasFlag = (name) => args.includes(`--${name}`);

const profile = getArg('profile') || 'general';
const input = getArg('input');
const noLlm = hasFlag('no-llm');

if (!input) {
  console.error('Usage: node cloak.js --profile <general|legal|financial|email|code|medical> --input <file_or_text>');
  process.exit(1);
}

let tmpFile = null;

try {
  const cliArgs = ['cloak'];
  let inputFile;

  if (existsSync(input)) {
    inputFile = input;
  } else {
    // Raw text — write to a temp file since CLI expects a file arg
    const tmp = mkdtempSync(join(tmpdir(), 'cloakclaw-'));
    tmpFile = join(tmp, 'input.txt');
    writeFileSync(tmpFile, input, 'utf-8');
    inputFile = tmpFile;
  }

  cliArgs.push(inputFile, '--profile', profile);
  if (noLlm) cliArgs.push('--no-llm');

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
