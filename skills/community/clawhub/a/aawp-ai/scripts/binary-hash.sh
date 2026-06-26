#!/usr/bin/env bash
# Compute canonical binary hash: SHA-256 of the binary with .ocx_entropy content zeroed.
# Pure Node.js ELF parser — no objcopy dependency, deterministic across all platforms.
# Usage: bash scripts/binary-hash.sh [path/to/aawp-core.node]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
NODE_FILE="${1:-$SCRIPT_DIR/../core/aawp-core.node}"

[ -f "$NODE_FILE" ] || { echo "ERROR: $NODE_FILE not found" >&2; exit 1; }

node -e "
const fs = require('fs');
const crypto = require('crypto');
const buf = Buffer.from(fs.readFileSync(process.argv[1]));

// Parse 64-bit LE ELF to find .ocx_entropy section and zero its content bytes
if (buf.length >= 64 && buf[0]===0x7f && buf[1]===0x45 && buf[2]===0x4c && buf[3]===0x46 && buf[4]===2) {
  const shoff = Number(buf.readBigUInt64LE(40));
  const shentsize = buf.readUInt16LE(58);
  const shnum = buf.readUInt16LE(60);
  const shstrndx = buf.readUInt16LE(62);

  const strSecBase = shoff + shstrndx * shentsize;
  const strOff = Number(buf.readBigUInt64LE(strSecBase + 24));
  const strSize = Number(buf.readBigUInt64LE(strSecBase + 32));

  for (let i = 0; i < shnum; i++) {
    const base = shoff + i * shentsize;
    const nameIdx = buf.readUInt32LE(base);
    let end = strOff + nameIdx;
    while (end < strOff + strSize && buf[end] !== 0) end++;
    const name = buf.slice(strOff + nameIdx, end).toString();
    if (name === '.ocx_entropy') {
      const secOff = Number(buf.readBigUInt64LE(base + 24));
      const secSize = Number(buf.readBigUInt64LE(base + 32));
      buf.fill(0, secOff, secOff + secSize);
      break;
    }
  }
}

process.stdout.write(crypto.createHash('sha256').update(buf).digest('hex'));
" "$NODE_FILE"
