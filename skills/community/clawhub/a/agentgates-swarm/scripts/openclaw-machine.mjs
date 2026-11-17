#!/usr/bin/env node
// Start, list, ask and renew OpenClaw agents on Agentgates computers: confidential
// ones (the default plan) or plain VMs for workers with nothing secret
// (--plan compute.vm.standard: no proof, its host can read it).
// No dependencies (Node 18 or newer). It spends only the prepaid balances behind
// the two keys its owner gave it. Before every purchase it asks the API for that
// purchase's exact price, and it refuses when --max-usd is missing, the price is
// over it, or the balance is short or unreadable.
//
//   node openclaw-machine.mjs price [--plan compute.standard] [--hours 1 | --minutes 30]
//   node openclaw-machine.mjs start --max-usd 1 [--name worker-1] [--plan ...] [--hours 1] [--model glm-5-3-flash]
//   node openclaw-machine.mjs list
//   node openclaw-machine.mjs ask <name> <message...> [--session <id>]
//   node openclaw-machine.mjs renew <name> --max-usd 1 [--hours 1 | --minutes 30]
//   node openclaw-machine.mjs body [--name ...] [--plan ...] [--hours 1] [--model ...]   (for an x402 client)
//   node openclaw-machine.mjs attach <name> <deploymentId> [endpoint]                 (after that x402 create)
//
// Keys (environment):
//   AGENTGATES_COMPUTE_KEY    agc_... on a prepaid compute balance: rents and renews machines, nothing else
//   AGENTGATES_INFERENCE_KEY  ag_... on a prepaid inference balance: the model key each new machine uses
//
// Each machine's gateway token is made here, sealed into that machine, and kept
// in --state (default ~/.agentgates/openclaw-machines.json, readable by you only).

import { randomBytes } from 'node:crypto';
import { chmodSync, closeSync, existsSync, mkdirSync, openSync, readFileSync, renameSync, statSync, unlinkSync, writeFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const COMPOSE_FILE = resolve(HERE, '..', 'compose.yml');

function parseArgs(argv) {
  const flags = {};
  const rest = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith('--')) flags[key] = true;
      else { flags[key] = next; i++; }
    } else rest.push(a);
  }
  return { flags, rest };
}

const { flags, rest } = parseArgs(process.argv.slice(2));
const command = rest.shift();
const API = String(flags.api || 'https://api.agentgates.ai').replace(/\/+$/, '');
const STATE = resolve(String(flags.state || join(homedir(), '.agentgates', 'openclaw-machines.json')));
const PLAN = String(flags.plan || 'compute.standard');
const MODEL = String(flags.model || 'glm-5-3-flash');

function fail(message) {
  console.error('error: ' + message);
  process.exit(1);
}

function timeAsked() {
  if (flags.minutes !== undefined) {
    const m = Number(flags.minutes);
    if (![15, 30, 45].includes(m)) fail('--minutes must be 15, 30 or 45');
    return { minutes: m };
  }
  const h = flags.hours === undefined ? 1 : Number(flags.hours);
  if (!Number.isInteger(h) || h < 1 || h > 720) fail('--hours must be a whole number from 1 to 720');
  return { hours: h };
}

function computeKey() {
  const key = process.env.AGENTGATES_COMPUTE_KEY;
  if (!key || !key.startsWith('agc_')) fail('AGENTGATES_COMPUTE_KEY must hold a compute key (agc_...) your owner minted on a prepaid compute balance');
  return key;
}

function inferenceKey() {
  const key = process.env.AGENTGATES_INFERENCE_KEY;
  if (!key || !key.startsWith('ag_')) fail('AGENTGATES_INFERENCE_KEY must hold an inference key (ag_...) on a prepaid inference balance');
  return key;
}

async function call(method, path, { key, body, timeoutMs = 60_000 } = {}) {
  const headers = { accept: 'application/json' };
  if (key) headers.authorization = 'Bearer ' + key;
  if (body !== undefined) headers['content-type'] = 'application/json';
  const res = await fetch(API + path, {
    method,
    headers,
    body: body === undefined ? undefined : JSON.stringify(body),
    signal: AbortSignal.timeout(timeoutMs),
  });
  const text = await res.text();
  let json = null;
  try { json = text ? JSON.parse(text) : null; } catch { /* not JSON */ }
  return { status: res.status, json, text };
}

function readState() {
  if (!existsSync(STATE)) return { machines: [] };
  try { return JSON.parse(readFileSync(STATE, 'utf8')); } catch { throw new Error('cannot read ' + STATE); }
}

function writeState(state) {
  mkdirSync(dirname(STATE), { recursive: true, mode: 0o700 });
  const tmp = STATE + '.' + process.pid + '.tmp';
  writeFileSync(tmp, JSON.stringify(state, null, 2) + '\n', { mode: 0o600 });
  renameSync(tmp, STATE);
  chmodSync(STATE, 0o600);
}

// One run at a time changes the state file, under a lock file made with O_EXCL,
// so runs side by side keep each other's machines and tokens. A lock older than
// 30 seconds was left by a run that died, and is taken over.
function locked(fn) {
  mkdirSync(dirname(STATE), { recursive: true, mode: 0o700 });
  const lock = STATE + '.lock';
  const deadline = Date.now() + 15_000;
  for (;;) {
    try {
      closeSync(openSync(lock, 'wx', 0o600));
      break;
    } catch (err) {
      if (err.code !== 'EEXIST') throw err;
      try { if (Date.now() - statSync(lock).mtimeMs > 30_000) unlinkSync(lock); } catch { /* released meanwhile */ }
      if (Date.now() > deadline) throw new Error('another run holds ' + lock + '; try again');
      Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 20);
    }
  }
  try { return fn(); } finally { try { unlinkSync(lock); } catch { /* already gone */ } }
}

// isNew claims the name: it refuses when another run saved that name first.
function saveMachine(fields, isNew = false) {
  const taken = locked(() => {
    const state = readState();
    const m = state.machines.find((x) => x.name === fields.name);
    if (m && isNew) return true;
    if (m) Object.assign(m, fields); else state.machines.push(fields);
    writeState(state);
    return false;
  });
  if (taken) fail('a machine named "' + fields.name + '" is already in ' + STATE);
}

function dropMachine(name) {
  locked(() => {
    const state = readState();
    state.machines = state.machines.filter((m) => m.name !== name);
    writeState(state);
  });
}

function freeName() {
  const name = String(flags.name || 'openclaw-' + randomBytes(3).toString('hex'));
  if (readState().machines.some((m) => m.name === name)) fail('a machine named "' + name + '" is already in ' + STATE);
  return name;
}

function findMachine(state, ref) {
  if (!ref) fail('name the machine: its --name or its deploymentId (see "list")');
  const m = state.machines.find((x) => x.name === ref || x.deploymentId === ref);
  if (!m) fail('no machine "' + ref + '" in ' + STATE);
  return m;
}

// The API's own price for this exact purchase: asked with no payment and no key,
// a create or a renewal answers 402 with one entry per network, and asking is
// free. A balance draw is charged the cheapest entry or less (compute docs).
async function quote(path, body) {
  const { status, json } = await call('POST', path, { body });
  // A plain plan sells while its host has room; out of room it answers 503.
  if (status === 503 && json && json.code === 'at_capacity') fail('no ' + PLAN + ' machine is free right now' + (json.error ? ' (' + json.error + ')' : '') + '; try again later or another plan; nothing was bought');
  if (status !== 402) fail('asking the price answered ' + status + (json && json.error ? ': ' + json.error : '') + '; nothing was bought');
  const legs = ((json && json.accepts) || []).map((a) => Number(a.maxAmountRequired) / 1e6).filter((n) => Number.isFinite(n) && n > 0);
  if (!legs.length) fail('the price answer named no amount; nothing was bought');
  return Math.min(...legs);
}

async function readBalance(key) {
  const { status, json } = await call('GET', '/api/compute/credits', { key });
  const c = json && (json.credit || json.balance || json);
  const v = Number(c && (c.availableUsd ?? c.balanceUsd));
  return status === 200 && Number.isFinite(v) && v >= 0 ? v : null;
}

// The owner's limit for one purchase. Required: there is no default budget.
function budget() {
  const cap = Number(flags['max-usd']);
  if (flags['max-usd'] === undefined || flags['max-usd'] === true || !Number.isFinite(cap) || cap <= 0) {
    fail('pass --max-usd <dollars>, the most your owner lets this purchase cost; nothing was bought');
  }
  return cap;
}

function guard(usd, cap, available) {
  if (usd > cap) fail('this costs $' + usd.toFixed(3) + ', over --max-usd ' + cap + '; nothing was bought');
  if (available === null) fail('the compute balance could not be read; nothing was bought');
  if (available < usd) {
    fail('the compute balance holds $' + available.toFixed(3) + ' and this costs $' + usd.toFixed(3) + '; ask your owner to top it up (POST ' + API + '/api/compute/credits); nothing was bought');
  }
}

// The API takes no cap of its own, so the charge is checked after the fact too.
function checkCharge(chargedUsd, cap) {
  if (chargedUsd !== null && chargedUsd > cap) {
    console.error('warning: charged $' + chargedUsd.toFixed(3) + ', over --max-usd ' + cap + ' (the price moved after the quote); tell your owner');
    process.exitCode = 2;
  }
}

function span(time) {
  return time.hours ? time.hours + ' hour(s)' : time.minutes + ' minutes';
}

function createBody(name, time, withEnv = true) {
  const body = { plan: PLAN, ...time, name, compose: readFileSync(COMPOSE_FILE, 'utf8') };
  if (withEnv) {
    body.env = {
      OPENCLAW_GATEWAY_TOKEN: randomBytes(32).toString('hex'),
      AGENTGATES_API_KEY: inferenceKey(),
      AGENTGATES_MODEL: MODEL,
    };
    // A plain VM's https name is a proxy inside the machine that reaches the
    // gateway from Docker's private range; OpenClaw answers a proxied call
    // only from a proxy it trusts. A confidential plan sends nothing new.
    if (PLAN.startsWith('compute.vm.')) body.env.OPENCLAW_TRUSTED_PROXIES = '172.16.0.0/12';
  }
  return body;
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function waitReady(key, machine) {
  const deadline = Date.now() + Number(flags['wait-minutes'] || 15) * 60_000;
  const said = new Set();
  const say = (line) => { if (!said.has(line)) { said.add(line); console.log(line); } };
  while (Date.now() < deadline) {
    const { status, json } = await call('GET', '/api/compute/deployments', { key });
    const row = status === 200 ? (json.deployments || []).find((d) => d.deploymentId === machine.deploymentId) : null;
    if (row) {
      say('machine ' + row.status);
      if (['failed', 'destroyed', 'grace', 'stopped'].includes(row.status)) fail('the machine is ' + row.status + '; see GET ' + API + '/api/compute/deployments');
      // A plain VM answers on its address first and on its https name once the
      // name's certificate is made inside it, about a minute later: wait for it.
      if (row.status === 'running' && row.endpoint && !row.endpoint.startsWith('https://') && row.aliasHost && row.aliasStatus !== 'live') {
        say('its https name ' + row.aliasHost + ' is not live yet');
      } else if (row.status === 'running' && row.endpoint) {
        machine.endpoint = row.endpoint;
        machine.expiresAt = row.expiresAt;
        const up = await fetch(row.endpoint.replace(/\/+$/, '') + '/startupz', { signal: AbortSignal.timeout(10_000) }).then((r) => r.status, () => 0);
        if (up === 200) return true;
        say('openclaw starting (it pulls its image and boots in a few minutes)');
      }
    }
    await sleep(10_000);
  }
  return false;
}

async function main() {
  if (command === 'price') {
    const time = timeAsked();
    const usd = await quote('/api/compute/deployments', createBody('price-check', time, false));
    const key = process.env.AGENTGATES_COMPUTE_KEY;
    const available = key ? await readBalance(key) : null;
    console.log(PLAN + ' for ' + span(time) + ': $' + usd.toFixed(3) + ' (quoted now; nothing was bought)');
    if (available !== null) console.log('compute balance available: $' + available.toFixed(3));
    return;
  }

  if (command === 'body') {
    const name = freeName();
    const body = createBody(name, timeAsked());
    saveMachine({ name, deploymentId: null, plan: PLAN, model: MODEL, token: body.env.OPENCLAW_GATEWAY_TOKEN, createdAt: new Date().toISOString(), paidWith: 'x402' }, true);
    process.stdout.write(JSON.stringify(body) + '\n');
    console.error('POST this body to ' + API + '/api/compute/deployments with your x402 client; then run: attach ' + name + ' <deploymentId>');
    return;
  }

  if (command === 'attach') {
    const m = findMachine(readState(), rest[0]);
    if (!rest[1]) fail('give the deploymentId the create answered');
    const fields = { name: m.name, deploymentId: rest[1] };
    // A machine another wallet paid for is not under your compute key: pass the
    // endpoint that wallet's own read of it answered.
    if (rest[2]) {
      if (!rest[2].startsWith('https://')) fail('the endpoint starts with https://');
      fields.endpoint = rest[2];
    }
    saveMachine(fields);
    console.log('saved ' + m.name + ' as ' + fields.deploymentId + (fields.endpoint ? ' at ' + fields.endpoint : ''));
    return;
  }

  if (command === 'start') {
    const key = computeKey();
    inferenceKey();
    const cap = budget();
    const time = timeAsked();
    const name = freeName();
    const usd = await quote('/api/compute/deployments', createBody(name, time, false));
    const available = await readBalance(key);
    console.log(PLAN + ' for ' + span(time) + ': $' + usd.toFixed(3) + ' quoted now, --max-usd ' + cap + ', compute balance ' + (available === null ? 'unreadable' : '$' + available.toFixed(3)));
    if (PLAN.startsWith('compute.vm.')) console.log('a plain VM: no proof; its host can read its env, the gateway token and the inference key included');
    guard(usd, cap, available);
    const body = createBody(name, time);
    const record = { name, deploymentId: null, plan: PLAN, model: MODEL, token: body.env.OPENCLAW_GATEWAY_TOKEN, createdAt: new Date().toISOString(), paidWith: 'balance' };
    saveMachine(record, true);
    const made = await call('POST', '/api/compute/deployments', { key, body, timeoutMs: 120_000 });
    if (made.status === 402) {
      dropMachine(name);
      fail('the balance did not cover it (402); nothing was bought');
    }
    if (made.status !== 202 && made.status !== 200) {
      dropMachine(name);
      fail('the create answered ' + made.status + ': ' + (made.json?.error || made.text).toString().slice(0, 300));
    }
    record.deploymentId = made.json.deploymentId;
    record.chargedUsd = made.json.charged?.amountMicro ? Number(made.json.charged.amountMicro) / 1e6 : null;
    saveMachine(record);
    console.log('bought ' + name + ' (' + record.deploymentId + ')' + (record.chargedUsd !== null ? ' for $' + record.chargedUsd.toFixed(3) : ''));
    checkCharge(record.chargedUsd, cap);
    if (flags['no-wait']) return;
    const ok = await waitReady(key, record);
    saveMachine(record);
    if (!ok) fail('not ready yet; run "list" later. If it never answers, its sealed env may be missing: see SKILL.md, "If a machine never answers"');
    console.log('ready: ' + record.endpoint + ' (until ' + record.expiresAt + ')');
    console.log('ask it: node ' + join(HERE, 'openclaw-machine.mjs') + ' ask ' + name + ' "your task"');
    return;
  }

  if (command === 'list') {
    const state = readState();
    const key = process.env.AGENTGATES_COMPUTE_KEY;
    const live = key ? await call('GET', '/api/compute/deployments', { key }) : null;
    const rows = live && live.status === 200 ? live.json.deployments || [] : [];
    for (const m of state.machines) {
      // A create whose answer was lost: the machine carries the name it was bought with.
      const row = rows.find((d) => d.deploymentId === m.deploymentId) || (!m.deploymentId ? rows.find((d) => d.name === m.name) : undefined);
      if (row) {
        m.deploymentId = row.deploymentId; m.endpoint = row.endpoint || m.endpoint; m.expiresAt = row.expiresAt;
        saveMachine({ name: m.name, deploymentId: m.deploymentId, endpoint: m.endpoint, expiresAt: m.expiresAt });
      }
      console.log([m.name, m.deploymentId || '(not bought yet)', row ? row.status : 'unknown', m.endpoint || '-', 'until ' + (m.expiresAt || '-')].join('  '));
    }
    return;
  }

  if (command === 'ask') {
    const state = readState();
    const m = findMachine(state, rest.shift());
    const message = rest.join(' ').trim();
    if (!message) fail('say what to ask');
    if (!m.endpoint) fail('no endpoint saved yet; run "list"');
    // The token is the machine's operator key: never sent in the clear.
    if (!m.endpoint.startsWith('https://')) fail('this machine has no https address yet (' + m.endpoint + '); its token is never sent in the clear: run "list" again in a minute');
    const res = await fetch(m.endpoint.replace(/\/+$/, '') + '/v1/chat/completions', {
      method: 'POST',
      headers: { authorization: 'Bearer ' + m.token, 'content-type': 'application/json' },
      body: JSON.stringify({ model: 'openclaw', user: String(flags.session || 'parent'), messages: [{ role: 'user', content: message }] }),
      signal: AbortSignal.timeout(Number(flags['timeout-minutes'] || 10) * 60_000),
    });
    const text = await res.text();
    let json = null;
    try { json = JSON.parse(text); } catch { /* not JSON */ }
    if (res.status !== 200) fail('the machine answered ' + res.status + ': ' + text.slice(0, 300));
    console.log(json?.choices?.[0]?.message?.content ?? text);
    return;
  }

  if (command === 'renew') {
    const key = computeKey();
    const state = readState();
    const m = findMachine(state, rest[0]);
    if (!m.deploymentId) fail('this machine was never bought');
    const cap = budget();
    const time = timeAsked();
    const path = '/api/compute/deployments/' + encodeURIComponent(m.deploymentId) + '/renew';
    const usd = await quote(path, time);
    const available = await readBalance(key);
    console.log('renewal for ' + span(time) + ': $' + usd.toFixed(3) + ' quoted now, --max-usd ' + cap + ', compute balance ' + (available === null ? 'unreadable' : '$' + available.toFixed(3)));
    guard(usd, cap, available);
    const r = await call('POST', path, { key, body: time });
    if (r.status === 402) fail('the balance did not cover the renewal (402); nothing was bought');
    if (r.status !== 200 && r.status !== 202) fail('the renewal answered ' + r.status + ': ' + (r.json?.error || r.text).toString().slice(0, 300));
    m.expiresAt = r.json.expiresAt || m.expiresAt;
    saveMachine({ name: m.name, expiresAt: m.expiresAt });
    const charged = r.json.charged && r.json.charged.amountMicro ? Number(r.json.charged.amountMicro) / 1e6 : null;
    console.log('renewed ' + m.name + ' until ' + m.expiresAt + (charged !== null ? ' for $' + charged.toFixed(3) : ''));
    checkCharge(charged, cap);
    return;
  }

  const lines = readFileSync(fileURLToPath(import.meta.url), 'utf8').split('\n').slice(1);
  console.log(lines.slice(0, lines.findIndex((l) => !l.startsWith('//'))).map((l) => l.replace(/^\/\/ ?/, '')).join('\n'));
  if (command && command !== 'help') process.exit(1);
}

main().catch((err) => fail(err && err.message ? err.message : String(err)));
