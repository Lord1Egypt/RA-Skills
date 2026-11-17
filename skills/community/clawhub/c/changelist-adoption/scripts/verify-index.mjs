#!/usr/bin/env node
// Verify a changelist index README against the entry files on disk.
// Fails (exit 1) when: a linked target is missing, an entry file is not linked
// (orphan), or a file is linked more than once. Exit 2 when no index exists.
// Usage: node verify-index.mjs <changelist-root>   (default: docs/changelist)
import fs from 'node:fs';
import path from 'node:path';

const root = process.argv[2] ?? 'docs/changelist';
const readmePath = path.join(root, 'README.md');
if (!fs.existsSync(readmePath)) {
  console.error(`no index README at ${readmePath}`);
  process.exit(2);
}
const readme = fs.readFileSync(readmePath, 'utf8');
const linked = [...readme.matchAll(/\]\((\d{8}\/[^)#?]+\.md)\)/g)].map((m) => m[1]);
const onDisk = [];
for (const dir of fs.readdirSync(root)) {
  if (!/^\d{8}$/.test(dir) || !fs.statSync(path.join(root, dir)).isDirectory()) continue;
  for (const file of fs.readdirSync(path.join(root, dir))) {
    if (file.endsWith('.md')) onDisk.push(`${dir}/${file}`);
  }
}
const missing = linked.filter((l) => !fs.existsSync(path.join(root, l)));
const orphans = onDisk.filter((f) => !linked.includes(f));
const dupes = linked.filter((l, i) => linked.indexOf(l) !== i);
console.log(`linked ${linked.length}, onDisk ${onDisk.length}`);
console.log(`missing: ${missing.length ? missing.join(', ') : 'none'}`);
console.log(`orphans: ${orphans.length ? orphans.join(', ') : 'none'}`);
console.log(`dupes: ${dupes.length ? dupes.join(', ') : 'none'}`);
process.exit(missing.length || orphans.length || dupes.length ? 1 : 0);
