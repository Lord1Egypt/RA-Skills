#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
const files = process.argv.slice(2);
if (!files.length) { console.error('Usage: node checksums.mjs <artifact> [artifact ...] > SHA256SUMS'); process.exit(1); }
const die = msg => { console.error(`checksums: ${msg}`); process.exit(1); };
const names = files.map(f => path.basename(f));
if (names.some(name => /^SHA256SUMS(?:\.txt)?$/i.test(name))) die('校验和不能包含自身；传入本次分发文件的明确列表');
if (new Set(names).size !== names.length || names.some(n => /[\r\n\\]/.test(n))) die('产物文件名冲突或含不支持字符');
const lines = [];
for (const file of [...files].sort((a, b) => path.basename(a).localeCompare(path.basename(b), 'en'))) {
  let stat;
  try { stat = fs.statSync(file); } catch (e) { die(`无法读取 ${file}: ${e.message.split('\n')[0]}`); }
  if (!stat || !stat.isFile()) die(`输入必须是文件: ${file}`);
  const hash = createHash('sha256');
  try {
    for await (const chunk of fs.createReadStream(file)) hash.update(chunk);
  } catch (e) { die(`无法读取 ${file}: ${e.message.split('\n')[0]}`); }
  lines.push(`${hash.digest('hex')}  ${path.basename(file)}\n`);
}
process.stdout.write(lines.join(''));
