#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { parseArgs, readJson, TIERS } from './lib/baton-common.mjs';
const args = parseArgs(process.argv.slice(2));
const dir = path.resolve(args.skillDir || args._[0] || '.');
let ok = true;
const pass=(m)=>console.log(`✅ ${m}`), warn=(m)=>console.log(`⚠ ${m}`), fail=(m)=>{ ok=false; console.error(`❌ ${m}`); };
const must = (rel)=> fs.existsSync(path.join(dir, rel)) ? pass(`${rel} exists`) : fail(`${rel} missing`);
const skillPath = path.join(dir, 'SKILL.md');
if (!fs.existsSync(skillPath)) fail('SKILL.md missing');
else {
  const skill = fs.readFileSync(skillPath,'utf8');
  const chars = skill.length;
  if (chars <= 6500) pass(`SKILL.md is token-efficient (${chars} chars)`); else warn(`SKILL.md is ${chars} chars; target <=6500`);
  if (/^---\n[\s\S]*?\n---/.test(skill)) pass('frontmatter present'); else fail('frontmatter missing');
  if (/^name:\s*baton\s*$/m.test(skill)) pass('frontmatter includes name'); else fail('frontmatter name missing or not baton');
  if (/^description:\s*.+/m.test(skill)) pass('frontmatter includes description'); else fail('frontmatter description missing');
  if (/^version:\s*1\.8\.2\s*$/m.test(skill)) pass('version is 1.8.2'); else fail('version is not 1.8.2');
  if (!/metadata:[\s\S]{0,300}requires[\s\S]{0,100}tools/.test(skill)) pass('frontmatter avoids non-standard requires.tools'); else fail('frontmatter contains non-standard requires.tools');
  for (const name of ['planner-orchestration','model-routing','rate-limits','model-management','model-discovery','role-taxonomy','patterns','permission-matrix','task-schema','prompts','resilience','conversation-management']) {
    if (skill.includes(name)) must(`references/${name}.md`);
  }
}
for (const rel of ['scripts/baton-setup.mjs','scripts/baton-model-manager.mjs','scripts/baton-status.mjs','scripts/baton-router.mjs','scripts/baton-model-select.mjs','scripts/lib/baton-common.mjs']) must(rel);
for (const rel of ['examples/model-allowlist.example.json','examples/rate-limits.example.json','examples/baton.config.example.json']) must(rel);
const allowPath = path.join(dir, '.openclaw/baton/model-allowlist.json');
if (fs.existsSync(allowPath)) {
  const allow = readJson(allowPath, null);
  for (const t of TIERS) if (allow?.tiers?.[t]) pass(`tier ${t} configured`); else fail(`tier ${t} missing`);
} else warn('model-allowlist.json not found; run baton-setup in the target workspace');
process.exit(ok ? 0 : 1);
