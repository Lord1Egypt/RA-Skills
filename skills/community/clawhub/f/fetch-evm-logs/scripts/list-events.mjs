#!/usr/bin/env node
/**
 * List event names from an ABI JSON file.
 * Usage: node list-events.mjs --abi path/to/abi_*.json
 */
import fs from 'fs';

function arg(name) {
  const i = process.argv.indexOf(`--${name}`);
  if (i >= 0 && process.argv[i + 1]) return process.argv[i + 1];
  return null;
}

const abiPath = arg('abi');
if (!abiPath || !fs.existsSync(abiPath)) {
  console.error('Usage: node list-events.mjs --abi <abi.json>');
  process.exit(1);
}

const abi = JSON.parse(fs.readFileSync(abiPath, 'utf8'));
const events = abi.filter((x) => x?.type === 'event');

if (!events.length) {
  console.log('No events in ABI.');
  process.exit(0);
}

console.log(`Found ${events.length} event(s):\n`);
for (const ev of events) {
  const inputs = (ev.inputs || [])
    .map((i) => `${i.indexed ? 'indexed ' : ''}${i.type} ${i.name || ''}`.trim())
    .join(', ');
  console.log(`- ${ev.name}(${inputs})`);
}
console.log('\nAsk the user: fetch all (*) or which event names?');
