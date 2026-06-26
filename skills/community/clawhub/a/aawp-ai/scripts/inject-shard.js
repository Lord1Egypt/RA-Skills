#!/usr/bin/env node
/**
 * Inject shard_B into .ocx_entropy section of aawp-core.node
 * Pure JS ELF manipulation — no objcopy, preserves file layout exactly.
 * 
 * Usage: node scripts/inject-shard.js <binary> <shard-file>
 */
'use strict';
const fs = require('fs');

const [,, binPath, shardPath] = process.argv;
if (!binPath || !shardPath) {
  console.error('Usage: node inject-shard.js <binary-path> <shard-file>');
  process.exit(1);
}

const buf = fs.readFileSync(binPath);
const shard = fs.readFileSync(shardPath);

if (shard.length < 16) {
  console.error(`ERROR: shard file too small (${shard.length} bytes, need >= 16)`);
  process.exit(1);
}

// Parse 64-bit LE ELF
if (buf.length < 64 || buf[0] !== 0x7f || buf[1] !== 0x45 || buf[2] !== 0x4c || buf[3] !== 0x46 || buf[4] !== 2) {
  console.error('ERROR: not a 64-bit ELF binary');
  process.exit(1);
}

const shoff = Number(buf.readBigUInt64LE(40));
const shentsize = buf.readUInt16LE(58);
const shnum = buf.readUInt16LE(60);
const shstrndx = buf.readUInt16LE(62);

const strSecBase = shoff + shstrndx * shentsize;
const strOff = Number(buf.readBigUInt64LE(strSecBase + 24));
const strSize = Number(buf.readBigUInt64LE(strSecBase + 32));

let found = false;
for (let i = 0; i < shnum; i++) {
  const base = shoff + i * shentsize;
  const nameIdx = buf.readUInt32LE(base);
  let end = strOff + nameIdx;
  while (end < strOff + strSize && buf[end] !== 0) end++;
  const name = buf.slice(strOff + nameIdx, end).toString();

  if (name === '.ocx_entropy') {
    const secOff = Number(buf.readBigUInt64LE(base + 24));
    const secSize = Number(buf.readBigUInt64LE(base + 32));

    if (secSize < 16) {
      console.error(`ERROR: .ocx_entropy section too small (${secSize} bytes)`);
      process.exit(1);
    }

    // Write shard bytes directly into the section (in-place, no layout change)
    shard.copy(buf, secOff, 0, Math.min(16, secSize));
    found = true;
    break;
  }
}

if (!found) {
  console.error('ERROR: .ocx_entropy section not found in binary');
  process.exit(1);
}

fs.writeFileSync(binPath, buf);
console.log(`✅ shard_B injected into ${binPath} (.ocx_entropy, 16 bytes)`);
