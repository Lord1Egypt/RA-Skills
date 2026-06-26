#!/usr/bin/env node
import path from 'node:path';
import { parseArgs, readJson, TIERS, resolveStateFile } from './lib/baton-common.mjs';
const args = parseArgs(process.argv.slice(2));
const root = path.resolve(args.outDir || '.openclaw/baton');
const discovered = readJson(path.join(root,'discovered-models.json'), { models: [] });
const allowPath = resolveStateFile(args, 'model-allowlist.json');
const cfgPath = resolveStateFile(args, 'baton.config.json');
const allow = readJson(allowPath, { allowedModels: [], tiers: {} });
const cfg = readJson(cfgPath, {});
const rate = readJson(resolveStateFile(args, 'rate-limits.json'), {});
console.log('Baton status\n');
console.log(`Execution mode: ${cfg.executionMode || '(not set)'}`);
console.log(`Allowlist: ${allowPath}`);
console.log(`Discovered models: ${discovered.models.length}`);
console.log(`Allowed models: ${allow.allowedModels.length}`);
console.log('\nTier coverage:');
for (const t of TIERS) {
  const n = (allow.tiers?.[t]?.models || []).length;
  console.log(`- ${t}: ${n ? '✅ ' + n : '⚠ empty'}`);
}
console.log('\nProvider limits:');
const providers = rate.providers || {};
if (!Object.keys(providers).length) console.log('- default policy only');
else for (const [p,v] of Object.entries(providers)) console.log(`- ${p}: ${JSON.stringify(v)}`);
