#!/usr/bin/env node
import path from 'node:path';
import { parseArgs, readJsonLike, readJson, writeJson, discoverConfiguredModels, discoverLiveModels, mergeDiscoveries, buildAllowlist, printGrouped, normalizeRef, TIERS, defaultRateLimits, batonPaths, resolveStateFile } from './lib/baton-common.mjs';

const args = parseArgs(process.argv.slice(2));
const cmd = args._[0] || 'help';
const paths = batonPaths(args);
const root = paths.root;
const activeRoot = paths.activeRoot;
const configPath = path.resolve(args.config || 'openclaw.json');
const discoveredPath = path.join(root, 'discovered-models.json');
const allowlistPath = args.allowlist ? path.resolve(args.allowlist) : (paths.agentId && (args.agentScoped || args.scoped) ? path.join(activeRoot, 'model-allowlist.json') : resolveStateFile(args, 'model-allowlist.json'));
const ratePath = args.rateLimits ? path.resolve(args.rateLimits) : resolveStateFile(args, 'rate-limits.json');

try { await main(); } catch (e) { console.error(`baton-model-manager: ${e.message}`); process.exit(1); }

async function main() {
  if (cmd === 'help' || args.help) return help();
  if (cmd === 'scan') return scan();
  if (cmd === 'list') return list();
  if (cmd === 'add') return add(args._[1]);
  if (cmd === 'remove') return remove(args._[1]);
  if (cmd === 'block') return block(args._[1]);
  if (cmd === 'unblock') return unblock(args._[1]);
  if (cmd === 'tier') return tier(args._[1], args._[2], args._[3]);
  if (cmd === 'prune-missing') return pruneMissing();
  if (cmd === 'rate') return rate(args._.slice(1));
  throw new Error(`unknown command: ${cmd}`);
}

function help() {
  console.log(`Usage:
  baton-model-manager.mjs scan --config openclaw.json --write [--no-live]
  baton-model-manager.mjs list
  baton-model-manager.mjs add provider/model --write
  baton-model-manager.mjs remove provider/model --write
  baton-model-manager.mjs block provider/model --write
  baton-model-manager.mjs unblock provider/model --write
  baton-model-manager.mjs tier <tier> add|remove provider/model --write
  baton-model-manager.mjs prune-missing --write
  baton-model-manager.mjs rate provider <id> maxConcurrent <n> --write
  baton-model-manager.mjs rate model <provider/model> maxConcurrent <n> --write

Options: --out-dir .openclaw/baton --agent-id main --agent-scoped --allowlist path`);
}
function loadDiscovered() { return readJson(discoveredPath, { models: [], groupedByProvider: {}, count: 0 }); }
function loadAllowlist() { return readJson(allowlistPath, buildAllowlist([], [])); }
function saveOrPrint(file, value) { if (args.write) { writeJson(file, value); console.log(`Wrote ${file}`); } else console.log(JSON.stringify(value, null, 2)); }

function scan() {
  const cfg = readJsonLike(configPath);
  const configured = discoverConfiguredModels(cfg, configPath);
  const live = args.noLive ? [] : discoverLiveModels();
  const merged = mergeDiscoveries(configured, live);
  if (args.write) writeJson(discoveredPath, merged);
  console.log(`Discovered ${merged.count} model(s).${live.length ? ` Live CLI returned ${live.length}.` : ''}`);
  printGrouped(merged);
  if (args.write) console.log(`\nWrote ${discoveredPath}`);
}

function list() {
  const discovered = loadDiscovered();
  const allow = loadAllowlist();
  console.log(`Discovered: ${discovered.count || discovered.models.length}`);
  printGrouped(discovered);
  console.log(`\nAllowed (${allow.allowedModels.length}):`);
  for (const ref of allow.allowedModels) console.log(`- ${ref}`);
  console.log('\nTiers:');
  for (const t of TIERS) console.log(`- ${t}: ${(allow.tiers?.[t]?.models || []).join(', ') || '(empty)'}`);
}
function add(ref) {
  const r = normalizeRef(ref); if (!r) throw new Error('provide provider/model');
  const discovered = loadDiscovered(); const allow = loadAllowlist();
  const selected = [...new Set([...allow.allowedModels, r])];
  const next = buildAllowlist(selected, discovered.models, allow);
  saveOrPrint(allowlistPath, next);
}
function remove(ref) {
  const r = normalizeRef(ref); if (!r) throw new Error('provide provider/model');
  const allow = loadAllowlist();
  const selected = allow.allowedModels.filter((x)=>x!==r);
  const next = buildAllowlist(selected, loadDiscovered().models, allow);
  for (const t of TIERS) next.tiers[t].models = next.tiers[t].models.filter((x)=>x!==r);
  saveOrPrint(allowlistPath, next);
}
function block(ref) {
  const r = normalizeRef(ref); if (!r) throw new Error('provide provider/model');
  const allow = loadAllowlist();
  allow.blockedModels = [...new Set([...(allow.blockedModels || []), r])].sort();
  saveOrPrint(allowlistPath, allow);
}
function unblock(ref) {
  const r = normalizeRef(ref); if (!r) throw new Error('provide provider/model');
  const allow = loadAllowlist();
  allow.blockedModels = (allow.blockedModels || []).filter((x)=>x!==r);
  saveOrPrint(allowlistPath, allow);
}
function tier(t, action, ref) {
  if (!TIERS.includes(t)) throw new Error(`tier must be one of: ${TIERS.join(', ')}`);
  const r = normalizeRef(ref); if (!r) throw new Error('provide provider/model');
  const allow = loadAllowlist();
  if (!allow.allowedModels.includes(r)) allow.allowedModels.push(r);
  allow.tiers ||= {}; allow.tiers[t] ||= { models: [], fallback: null, maxAttempts: 2 };
  if (action === 'add') allow.tiers[t].models = [...new Set([...(allow.tiers[t].models || []), r])];
  else if (action === 'remove') allow.tiers[t].models = (allow.tiers[t].models || []).filter((x)=>x!==r);
  else throw new Error('tier action must be add or remove');
  saveOrPrint(allowlistPath, buildAllowlist(allow.allowedModels, loadDiscovered().models, allow));
}
function pruneMissing() {
  const discovered = new Set(loadDiscovered().models.map((m)=>m.ref));
  const allow = loadAllowlist();
  const kept = allow.allowedModels.filter((ref)=>discovered.has(ref));
  const next = buildAllowlist(kept, loadDiscovered().models, allow);
  saveOrPrint(allowlistPath, next);
}
function rate(parts) {
  const [scope, id, key, value] = parts;
  if (!['provider','model'].includes(scope)) throw new Error('rate scope must be provider or model');
  if (!id || !key || value === undefined) throw new Error('usage: rate provider <id> maxConcurrent <n> --write');
  const policy = readJson(ratePath, defaultRateLimits());
  const bucket = scope === 'provider' ? 'providers' : 'models';
  policy[bucket] ||= {}; policy[bucket][id] ||= {};
  const normalizedKey = key === 'maxConcurrent' ? 'maxConcurrent' : key;
  policy[bucket][id][normalizedKey] = /^\d+$/.test(String(value)) ? Number(value) : value;
  saveOrPrint(ratePath, policy);
}
