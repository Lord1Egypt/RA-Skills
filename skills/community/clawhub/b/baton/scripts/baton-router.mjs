#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { parseArgs, readJson, writeJson, providerOf, defaultRateLimits, resolveStateFile } from './lib/baton-common.mjs';

const args = parseArgs(process.argv.slice(2));
const cmd = args._[0] || 'help';
const root = path.resolve(args.outDir || '.openclaw/baton');
const allowPath = args.allowlist ? path.resolve(args.allowlist) : resolveStateFile(args, 'model-allowlist.json');
const ratePath = args.rateLimits ? path.resolve(args.rateLimits) : resolveStateFile(args, 'rate-limits.json');
const statePath = path.resolve(args.state || path.join(root, 'runtime/rate-state.json'));
const lockPath = `${statePath}.lock`;
try { await main(); } catch(e) { console.error(`baton-router: ${e.message}`); process.exit(1); }

async function main() {
  if (cmd === 'help' || args.help) return help();
  if (cmd === 'route') return withLock(()=>route());
  if (cmd === 'release') return withLock(()=>release(args.leaseId));
  if (cmd === 'cooldown') return withLock(()=>cooldown(args.model || args._[1], args.reason || 'manual'));
  if (cmd === 'state') return console.log(JSON.stringify(readState(), null, 2));
  throw new Error(`unknown command ${cmd}`);
}
function help(){ console.log(`Usage:
  baton-router.mjs route --tier balanced --role researcher --agent-id main --task taskName [--lease]
  baton-router.mjs release --lease-id <id>
  baton-router.mjs cooldown provider/model --reason 429
  baton-router.mjs state

Per-agent allowlists are used automatically when .openclaw/baton/agents/<agent-id>/model-allowlist.json exists.`); }
function route(){
  const allow = readJson(allowPath, null); if (!allow) throw new Error('model-allowlist.json not found');
  const policy = readJson(ratePath, defaultRateLimits());
  const state = cleanup(readState(), policy);
  const tier = args.tier || allow.roles?.[args.role]?.preferredTier || 'balanced';
  const candidates = collectCandidates(allow, tier);
  const selected = candidates.find((ref)=>canUse(ref, policy, state));
  if (!selected) {
    const result = { status:'blocked', tier, candidates, reason:'all candidates are at concurrency limit or cooling down' };
    writeState(state); console.log(JSON.stringify(result, null, 2)); return;
  }
  let lease = null;
  if (args.lease) {
    lease = { id: `${Date.now()}-${Math.random().toString(36).slice(2,8)}`, model:selected, provider:providerOf(selected), agentId:args.agentId || 'main', task:args.task || args.taskName || null, createdAt:Date.now(), expiresAt:Date.now() + (policy.defaults?.leaseTtlMs || 900000) };
    state.leases ||= []; state.leases.push(lease); writeState(state);
  } else writeState(state);
  console.log(JSON.stringify({ status:'ok', model:selected, provider:providerOf(selected), tier, lease }, null, 2));
}
function collectCandidates(allow, tier){
  const seen = new Set(), out = [];
  let t = tier, guard = 0;
  while (t && guard++ < 10) {
    for (const ref of allow.tiers?.[t]?.models || []) if (!seen.has(ref) && allow.allowedModels?.includes(ref) && !(allow.blockedModels||[]).includes(ref)) { seen.add(ref); out.push(ref); }
    t = allow.tiers?.[t]?.fallback;
  }
  return out;
}
function canUse(ref, policy, state){
  const now = Date.now(), p = providerOf(ref);
  const cd = state.cooldowns || {};
  if ((cd[p] || 0) > now || (cd[ref] || 0) > now) return false;
  const activeP = (state.leases || []).filter((l)=>l.provider===p).length;
  const activeM = (state.leases || []).filter((l)=>l.model===ref).length;
  const pLimit = policy.providers?.[p]?.maxConcurrent ?? policy.defaults?.maxConcurrentPerProvider ?? 4;
  const mLimit = policy.models?.[ref]?.maxConcurrent ?? policy.defaults?.maxConcurrentPerModel ?? 2;
  return activeP < pLimit && activeM < mLimit;
}
function release(id){ if (!id) throw new Error('--lease-id required'); const state=readState(); const before=(state.leases||[]).length; state.leases=(state.leases||[]).filter((l)=>l.id!==id); writeState(state); console.log(JSON.stringify({status:'ok', released: before-state.leases.length}, null, 2)); }
function cooldown(ref, reason){ if (!ref) throw new Error('provide provider/model'); const policy=readJson(ratePath, defaultRateLimits()); const state=readState(); const ms = reason === 'timeout' ? (policy.defaults?.cooldownMsAfterTimeout || 60000) : (policy.providers?.[providerOf(ref)]?.cooldownMsAfter429 || policy.defaults?.cooldownMsAfter429 || 120000); state.cooldowns ||= {}; state.cooldowns[ref]=Date.now()+ms; state.cooldowns[providerOf(ref)]=Math.max(state.cooldowns[providerOf(ref)]||0, Date.now()+Math.floor(ms/2)); writeState(state); console.log(JSON.stringify({status:'ok', model:ref, cooldownMs:ms}, null, 2)); }
function cleanup(state, policy){ const now=Date.now(); state.leases=(state.leases||[]).filter((l)=>(l.expiresAt||0)>now); state.cooldowns=Object.fromEntries(Object.entries(state.cooldowns||{}).filter(([,until])=>until>now)); return state; }
function readState(){ return readJson(statePath, { version:1, leases:[], cooldowns:{} }); }
function writeState(s){ writeJson(statePath, s); }
async function withLock(fn){
  fs.mkdirSync(path.dirname(lockPath), {recursive:true});
  const start=Date.now();
  while (true) {
    try { const fd=fs.openSync(lockPath, 'wx'); fs.writeFileSync(fd, String(process.pid)); fs.closeSync(fd); break; }
    catch { if (Date.now()-start > 5000) throw new Error('could not acquire rate-state lock'); await new Promise(r=>setTimeout(r,50)); }
  }
  try { return fn(); } finally { try { fs.unlinkSync(lockPath); } catch {} }
}
