#!/usr/bin/env node
// AgentAlarm for AI agents: pair this computer with the iPhone app, then ring encrypted alarms through the relay.
//   agentalarm pair <CODE> [--name "My gateway"] [--relay URL]
//   agentalarm ring "<alarm text>" [--id ID]
//   agentalarm status
//   agentalarm unpair
// Config: ~/.config/agentalarm/config.json (mode 600; NanoClaw: /workspace/agent/.agentalarm), or $AGENTALARM_CONFIG. Node stdlib only.
import { randomUUID } from 'node:crypto';
import { chmodSync, existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { homedir, hostname } from 'node:os';
import { dirname, join } from 'node:path';
import { parseArgs } from 'node:util';
import { seal } from './crypto.mjs';

// NanoClaw runs each session in a fresh container that keeps only the agent group's folder, so pair there.
const NANOCLAW = existsSync('/app/.nanoclaw-session.json');
// AGENTALARM_CONFIG moves the pairing file, e.g. into a folder a containerised agent keeps between runs.
const CONFIG = process.env.AGENTALARM_CONFIG
  ?? (NANOCLAW ? '/workspace/agent/.agentalarm/config.json' : join(homedir(), '.config/agentalarm/config.json'));
const DEFAULT_RELAY = process.env.AGENTALARM_RELAY ?? 'https://api.agentalarm.app';

const { positionals, values } = parseArgs({
  allowPositionals: true,
  options: { name: { type: 'string' }, relay: { type: 'string' }, id: { type: 'string' } },
});
const [command, ...rest] = positionals;

const die = (msg) => { console.error(`agentalarm: ${msg}`); process.exit(1); };
const load = () => (existsSync(CONFIG) ? JSON.parse(readFileSync(CONFIG, 'utf8')) : die('not paired. Run: agentalarm pair <CODE>'));
function save(config) {
  mkdirSync(dirname(CONFIG), { recursive: true, mode: 0o700 });
  writeFileSync(CONFIG, JSON.stringify(config, null, 2), { mode: 0o600 });
  chmodSync(CONFIG, 0o600);
}
// Names the connection after the agent running this command, as the app lists it. Only signals the agents set
// themselves count (same list as Vercel's @vercel/detect-agent); anything else is just "Your agent".
// OpenClaw and Hermes come first because they run another agent underneath (OpenClaw often runs Claude Code).
function agentName() {
  if (NANOCLAW) {
    // The hostname is the container's id, so use the assistant's name instead.
    const config = existsSync('/workspace/agent/container.json') ? JSON.parse(readFileSync('/workspace/agent/container.json', 'utf8')) : {};
    return config.assistantName ? `NanoClaw (${config.assistantName})` : 'NanoClaw';
  }
  const e = process.env;
  const agent = e.HERMES_SESSION_ID ? 'Hermes'
    : Object.keys(e).some((k) => k.startsWith('OPENCLAW_')) ? 'OpenClaw'
    : e.CLAUDECODE || e.CLAUDE_CODE ? 'Claude Code'
    : e.CODEX_THREAD_ID || e.CODEX_SANDBOX || e.CODEX_CI ? 'Codex'
    : e.GEMINI_CLI ? 'Gemini CLI'
    : e.CURSOR_AGENT || e.CURSOR_TRACE_ID ? 'Cursor'
    : e.OPENCODE === '1' || e.OPENCODE_CLIENT ? 'OpenCode'
    : e.AUGMENT_AGENT ? 'Augment'
    : null;
  return agent ? `${agent} on ${hostname().replace(/\.local$/, '')}` : 'Your agent';
}
async function call(relay, method, path, { body, auth } = {}) {
  let res;
  try {
    res = await fetch(relay + path, {
      method,
      headers: { 'content-type': 'application/json', ...(auth && { authorization: `Bearer ${auth}` }) },
      body: body && JSON.stringify(body),
      signal: AbortSignal.timeout(15_000),
    });
  } catch (e) {
    die(`can't reach the relay at ${relay} (${e.cause?.code ?? e.message})`);
  }
  const json = await res.json().catch(() => ({}));
  if (!res.ok) die(json.error ?? `relay returned ${res.status}`);
  return json;
}

switch (command) {
  case 'pair': {
    const code = rest[0] ?? die(`usage: agentalarm pair <CODE> [--name NAME] (code from AgentAlarm › Connect an agent; default name \"${agentName()}\")`);
    const relay = (values.relay ?? DEFAULT_RELAY).replace(/\/$/, '');
    const name = values.name ?? agentName();
    const r = await call(relay, 'POST', '/v1/pair', { body: { code, name } });
    save({ relay, name, pairingId: r.pairingId, sendToken: r.sendToken, devicePublicKey: r.devicePublicKey, pairedAt: new Date().toISOString() });
    console.log(`paired as "${name}". Test it: agentalarm ring "Test alarm"`);
    break;
  }
  case 'ring': {
    const text = rest.join(' ').trim() || die('usage: agentalarm ring "<alarm text>"');
    if (text.length > 500) die('alarm text is limited to 500 characters');
    const c = load();
    const id = values.id ?? randomUUID();
    const box = seal(c.devicePublicKey, { t: text, at: new Date().toISOString() });
    await call(c.relay, 'POST', '/v1/alarms', { auth: c.sendToken, body: { id, ...box } });
    console.log(`alarm sent: ${text}`);
    break;
  }
  case 'status': {
    const c = load();
    console.log(`paired as "${c.name}" since ${c.pairedAt}\nrelay: ${c.relay}`);
    break;
  }
  case 'unpair': {
    const c = load();
    await call(c.relay, 'DELETE', `/v1/pairings/${c.pairingId}`, { auth: c.sendToken });
    rmSync(CONFIG);
    console.log('unpaired');
    break;
  }
  default:
    die('usage: agentalarm pair <CODE> | ring "<text>" | status | unpair');
}
