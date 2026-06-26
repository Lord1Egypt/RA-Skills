#!/usr/bin/env node
'use strict';
const ra = require('../index.js');
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const cmd = args[0];

function flag(names, def) {
  for (const n of names) {
    const i = args.indexOf(n);
    if (i !== -1 && args[i + 1] !== undefined) return args[i + 1];
  }
  return def;
}
function has(name) { return args.includes(name); }

function printSkill(i, s) {
  console.log(`${i}. \x1b[1m${s.name || '?'}\x1b[0m`);
  console.log(`   Identifier:  ${s.identifier || ''}`);
  console.log(`   Description: ${s.description || 'No description.'}`);
  console.log(`   Source:      \x1b[36m${s.source || ''}\x1b[0m  |  Category: \x1b[35m${s.category || ''}\x1b[0m`);
  if (s.installCmd) console.log(`   Install:     \x1b[33m${s.installCmd}\x1b[0m`);
  if (s.sourceUrl) console.log(`   URL:         ${s.sourceUrl}`);
  console.log('-'.repeat(60));
}

function usage() {
  console.log(`ra-skills — search 90,896 Hermes Agent skills offline

Usage:
  ra-skills search <query> [-s source] [-c category] [-l limit]
  ra-skills show <name>
  ra-skills stats
  ra-skills list [-s source] [-c category] [-l limit]
  ra-skills get <name> [-o dir] [--md-only]
  ra-skills --version`);
}

async function main() {
  if (has('--version')) { console.log(`ra-skills ${require('../package.json').version}`); return; }
  const opts = { source: flag(['-s', '--source']), category: flag(['-c', '--category']), limit: parseInt(flag(['-l', '--limit'], '10'), 10) };

  if (cmd === 'search') {
    const q = args[1] && !args[1].startsWith('-') ? args[1] : null;
    const all = ra.search(q, { ...opts, limit: 0 });
    const shown = all.slice(0, opts.limit);
    console.log(`\nFound ${all.length} matching skills (showing ${shown.length}):\n`);
    shown.forEach((s, i) => printSkill(i + 1, s));
  } else if (cmd === 'show') {
    const s = ra.show(args[1]);
    if (!s) { console.log(`Skill '${args[1]}' not found.`); process.exit(1); }
    printSkill(1, s);
  } else if (cmd === 'stats') {
    const st = ra.stats();
    console.log('=== RA-Skills Registry ===');
    console.log(`Total:     ${st.total.toLocaleString()}`);
    console.log(`Built-in:  ${st.built_in.toLocaleString()}`);
    console.log(`Optional:  ${st.optional.toLocaleString()}`);
    console.log(`Community: ${st.community.toLocaleString()}`);
    console.log('By source:');
    for (const [k, v] of Object.entries(st.by_source)) console.log(`  ${k.padEnd(12)} ${v.toLocaleString()}`);
  } else if (cmd === 'list') {
    const res = ra.search(null, { ...opts, limit: parseInt(flag(['-l', '--limit'], '20'), 10) });
    res.forEach((s, i) => console.log(`${String(i + 1).padStart(4)}. ${(s.name || '').padEnd(40)}  [${s.source || ''}]`));
  } else if (cmd === 'get') {
    const name = args[1];
    const out = flag(['-o', '--output']);
    if (has('--md-only')) {
      const content = await ra.fetchContent(name);
      if (!content) { console.log(`Could not fetch SKILL.md for '${name}'.`); process.exit(1); }
      if (out) { fs.writeFileSync(out, content); console.log(`Saved ${content.length} bytes to ${out}`); }
      else console.log(content);
    } else {
      const dir = await ra.download(name, out || '.');
      if (!dir) { console.log(`Could not download '${name}'.`); process.exit(1); }
      let n = 0;
      const walk = (d) => fs.readdirSync(d, { withFileTypes: true }).forEach((e) => e.isDirectory() ? walk(path.join(d, e.name)) : n++);
      walk(dir);
      console.log(`Downloaded full skill folder → ${dir}  (${n} files)`);
    }
  } else {
    usage();
  }
}

main().catch((e) => { console.error(e.message); process.exit(1); });
