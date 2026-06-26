#!/usr/bin/env node
import path from 'node:path';
import readline from 'node:readline/promises';
import { stdin as input, stdout as output } from 'node:process';
import { parseArgs, readJsonLike, writeJson, discoverConfiguredModels, discoverLiveModels, mergeDiscoveries, printGrouped, buildAllowlist, defaultRateLimits, defaultBatonConfig, TIERS, batonPaths } from './lib/baton-common.mjs';

const args = parseArgs(process.argv.slice(2));
const paths = batonPaths(args);
const root = paths.root;
const activeRoot = paths.activeRoot;
const configPath = path.resolve(args.config || 'openclaw.json');
const agentId = args.agentId || 'main';
const discoveredPath = path.join(root, 'discovered-models.json');
const allowlistPath = path.join(activeRoot, 'model-allowlist.json');
const configOutPath = path.join(activeRoot, 'baton.config.json');
const ratePath = path.join(root, 'rate-limits.json');

try { await main(); } catch(e) { console.error(`baton-setup: ${e.message}`); process.exit(1); }

async function main() {
  const cfg = readJsonLike(configPath);
  const configured = discoverConfiguredModels(cfg, configPath);
  const live = args.noLive ? [] : discoverLiveModels();
  const discovered = mergeDiscoveries(configured, live);
  writeJson(discoveredPath, discovered);
  console.log(`Discovered ${discovered.count} model(s).`);
  printGrouped(discovered);
  let selected;
  if (args.all) selected = discovered.models.map((m)=>m.ref);
  else if (args.select) selected = String(args.select).split(',').map((s)=>s.trim()).filter(Boolean);
  else selected = await ask(discovered.models.map((m)=>m.ref));
  const allow = buildAllowlist(selected, discovered.models);
  allow.scope = paths.activeRoot === paths.root ? 'global' : `agent:${agentId}`;
  if (!args.noTierPrompt) await tierPrompt(allow, selected);
  writeJson(allowlistPath, allow);
  writeJson(configOutPath, defaultBatonConfig(agentId));
  writeJson(ratePath, defaultRateLimits());
  console.log(`\nWrote:\n- ${discoveredPath}\n- ${allowlistPath}\n- ${configOutPath}\n- ${ratePath}`);
}
async function ask(refs) {
  const rl = readline.createInterface({ input, output });
  const answer = await rl.question('\nSelect models Baton may use by number, refs, or all: ');
  rl.close();
  const text = answer.trim();
  if (!text || text.toLowerCase() === 'all') return refs;
  if (/^\d+(\s*,\s*\d+)*$/.test(text)) return text.split(',').map((n)=>refs[Number(n.trim())-1]).filter(Boolean);
  return text.split(',').map((s)=>s.trim()).filter(Boolean);
}
async function tierPrompt(allow, refs) {
  if (!process.stdin.isTTY) return;
  const rl = readline.createInterface({ input, output });
  console.log('\nOptional: assign tier models by numbers/refs, or press Enter to keep suggestions.');
  for (const tier of TIERS) {
    const current = allow.tiers[tier].models.join(', ') || '(empty)';
    const ans = await rl.question(`${tier} [${current}]: `);
    if (!ans.trim()) continue;
    allow.tiers[tier].models = parseSelection(ans, refs);
  }
  rl.close();
}
function parseSelection(text, refs) {
  if (/^\d+(\s*,\s*\d+)*$/.test(text.trim())) return text.split(',').map((n)=>refs[Number(n.trim())-1]).filter(Boolean);
  return text.split(',').map((s)=>s.trim().toLowerCase()).filter(Boolean);
}
