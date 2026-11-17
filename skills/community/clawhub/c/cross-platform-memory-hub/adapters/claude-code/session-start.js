#!/usr/bin/env node
/**
 * Safe template: session-start.js
 * Default behavior: no read unless user has explicitly enabled it with MEMORY_HUB_USER_CONFIRMED=1 and MEMORY_HUB_ENABLE_READ=1.
 * The script reads only a user-approved file path provided by MEMORY_HUB_READ_FILE.
 */

const fs = require('fs');
const path = require('path');

const ENABLED = process.env.MEMORY_HUB_USER_CONFIRMED === '1' && process.env.MEMORY_HUB_ENABLE_READ === '1';
const readFile = process.env.MEMORY_HUB_READ_FILE || '';

function sanitize(value) {
  return String(value || '')
    .replace(/(token|secret|password|key)\s*[:=]\s*\S+/gi, '$1=[REDACTED]')
    .replace(/-----BEGIN[\s\S]*?-----END[^-]+-----/g, '[REDACTED_KEY_BLOCK]');
}

function main() {
  if (!ENABLED) {
    console.log('[memory-hub] read disabled. Set MEMORY_HUB_USER_CONFIRMED=1 and MEMORY_HUB_ENABLE_READ=1 after user consent.');
    return;
  }

  if (!readFile || !fs.existsSync(readFile) || !fs.statSync(readFile).isFile()) {
    console.error('[memory-hub] MEMORY_HUB_READ_FILE must point to one user-approved file.');
    return;
  }

  const content = sanitize(fs.readFileSync(path.resolve(readFile), 'utf-8'));
  console.log(`\nCross-platform memory loaded from approved file:\n\n${content}\n`);
}

main();