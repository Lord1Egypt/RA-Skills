#!/usr/bin/env node
/**
 * Ava OpenClaw CLI: thin HTTP client over Ava MCP + REST.
 * Zero dependencies (Node 20+ fetch). Testnet is the default mode.
 *
 * Usage:
 *   node scripts/ava.mjs session
 *   node scripts/ava.mjs tools
 *   node scripts/ava.mjs call ava_create_mandate '{"portal":"base","message":"..."}'
 *   node scripts/ava.mjs lend <mandateId>
 *   node scripts/ava.mjs lend <mandateId> <previewHash>
 *   node scripts/ava.mjs turn "Swap 10 USDC to WETH on base with 50 bps slip"  # testnet only
 *   node scripts/ava.mjs approve <executionId>  # testnet only
 *   node scripts/ava.mjs portfolio
 *   node scripts/ava.mjs price USDC
 *   node scripts/ava.mjs call ava_list_mandates '{}'
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { homedir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const STATE_DIR = join(homedir(), ".config", "ava-openclaw");
const STATE_FILE = join(STATE_DIR, "state.json");

function env(name, fallback = "") {
  const v = process.env[name];
  return v !== undefined && v.trim().length > 0 ? v.trim() : fallback;
}

function loadState() {
  try {
    if (!existsSync(STATE_FILE)) return {};
    return JSON.parse(readFileSync(STATE_FILE, "utf8"));
  } catch {
    return {};
  }
}

function saveState(partial) {
  mkdirSync(STATE_DIR, { recursive: true });
  const next = { ...loadState(), ...partial, updatedAt: new Date().toISOString() };
  writeFileSync(STATE_FILE, JSON.stringify(next, null, 2), { mode: 0o600 });
  return next;
}

function baseUrl() {
  return env("AVA_API_BASE", "https://api.getava.xyz").replace(/\/$/, "");
}

function portal() {
  return env("AVA_PORTAL", loadState().portal ?? "base").toLowerCase();
}

function userId() {
  return env("AVA_USER_ID", loadState().userId ?? "");
}

/**
 * The bearer credential. The user id names an account; this proves we hold it.
 * Ava derives the caller from this token server-side, so a userId passed in a
 * tool argument can only ever agree with it, never widen it.
 */
function token() {
  return env("AVA_TOKEN", loadState().token ?? "");
}

function requireUserId() {
  const id = userId();
  if (!id) {
    fail(
      "AVA_USER_ID missing. Run: node scripts/ava.mjs session\nOr export AVA_USER_ID=usr_...",
    );
  }
  return id;
}

function requireToken() {
  const value = token();
  if (!value) {
    fail(
      "No Ava session token. Run: node scripts/ava.mjs session\nOr export AVA_TOKEN=ava_st_...\nA user id on its own is not a credential and the API will refuse it.",
    );
  }
  return value;
}

function fail(msg, code = 1) {
  console.error(msg);
  process.exit(code);
}

async function http(method, path, { body, headers, auth = true } = {}) {
  const url = `${baseUrl()}${path}`;
  const bearer = auth ? token() : "";
  const res = await fetch(url, {
    method,
    headers: {
      "content-type": "application/json",
      accept: "application/json",
      ...(bearer ? { authorization: `Bearer ${bearer}` } : {}),
      ...(headers ?? {}),
    },
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  let json;
  try {
    json = text ? JSON.parse(text) : null;
  } catch {
    json = { raw: text };
  }
  if (!res.ok) {
    const err = new Error(
      `HTTP ${res.status} ${method} ${path}: ${typeof json === "object" ? JSON.stringify(json) : text}`,
    );
    err.status = res.status;
    err.body = json;
    throw err;
  }
  return json;
}

async function mcpCall(name, args = {}) {
  const body = await http("POST", "/mcp", {
    body: {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name, arguments: args },
    },
  });
  if (body?.error) {
    return { ok: false, error: body.error };
  }
  return body?.result?.structuredContent ?? body?.result ?? body;
}

function printJson(value) {
  console.log(JSON.stringify(value, null, 2));
}

async function cmdSession() {
  const displayName = env("AVA_DISPLAY_NAME", "openclaw-agent");
  // Deliberately unauthenticated: this is the call that hands out credentials,
  // and Ava's machine onboarding has no CAPTCHA, email, or wallet popup.
  const body = await http("POST", "/v1/users/session", {
    body: { displayName },
    auth: false,
  });
  const id =
    body?.user?.userId ??
    body?.userId ??
    body?.user?.id ??
    null;
  if (!id) {
    fail(`Session response missing userId: ${JSON.stringify(body)}`);
  }
  const issued = body?.token ?? null;
  if (!issued && !token()) {
    fail(
      `Session response carried no token and none is stored. Every other call needs one, so stopping here rather than making requests that will be refused: ${JSON.stringify(body)}`,
    );
  }
  // Written with mode 0600 by saveState. Treat this file as a secret.
  saveState({ userId: id, portal: portal(), ...(issued ? { token: issued } : {}) });
  printJson({
    ok: true,
    userId: id,
    portal: portal(),
    stateFile: STATE_FILE,
    tokenStored: Boolean(issued),
    note: "The token is stored in the state file (mode 0600) and is not printed here. It is shown by the API once and cannot be read back. Every other command sends it as Authorization: Bearer.",
    session: { ...body, token: issued ? "[stored, not printed]" : undefined },
  });
}

async function cmdTools() {
  const doc = await http("GET", "/mcp", { auth: false });
  const names = (doc.tools ?? []).map((t) => t.name);
  printJson({ ok: true, base: baseUrl(), tools: names, server: doc.server });
}

async function cmdTurn(message) {
  if (!message || !message.trim()) {
    fail('Usage: ava turn "Swap 10 USDC to WETH on base with 50 bps slip"  (testnet only)');
  }
  const uid = requireUserId();
  requireToken();
  const result = await mcpCall("ava_copilot_turn", {
    message: message.trim(),
    portal: portal(),
    userId: uid,
    mode: "testnet",
  });
  const actions = result?.actions ?? [];
  const approve = actions.find((a) => a?.type === "approve_execute");
  if (approve?.executionId) {
    saveState({ lastExecutionId: approve.executionId, userId: uid });
  }
  printJson({
    ...result,
    _hint:
      approve?.executionId !== undefined
        ? `TESTNET ONLY. Review quote. If user says yes: node scripts/ava.mjs approve ${approve.executionId}. Live capital is: node scripts/ava.mjs lend <mandateId>`
        : "No approve_execute action (parse failed or no trade). Do not invent a fill. Live capital is ava_lend_execute, not copilot.",
  });
}

async function cmdLend(mandateId, previewHash) {
  const id = mandateId || loadState().lastMandateId;
  if (!id) {
    fail(
      "Usage: ava lend <mandateId> [previewHash]\nFirst call omits previewHash and returns the artifact to show the human. Second call passes the returned previewHash. Live loop only.",
    );
  }
  const uid = requireUserId();
  requireToken();
  const args = {
    mandateId: id,
    userId: uid,
    portal: portal(),
  };
  if (previewHash && previewHash.trim()) {
    args.previewHash = previewHash.trim();
  }
  const result = await mcpCall("ava_lend_execute", args);
  saveState({ lastMandateId: id, userId: uid });
  const hash =
    result?.previewHash ??
    result?.preview?.previewHash ??
    result?.artifact?.previewHash ??
    null;
  printJson({
    ...result,
    _hint: previewHash
      ? "Return the receipt. Success is proof.standing: chain-confirmed. verified:true with unconfirmed standing is not a fill."
      : hash
        ? `Show this preview to the human. If they say yes: node scripts/ava.mjs lend ${id} ${hash}`
        : "Show this preview to the human. If they say yes, call again with the returned previewHash.",
  });
}

async function cmdApprove(executionId) {
  const id = executionId || loadState().lastExecutionId;
  if (!id) {
    fail("Usage: ava approve <executionId> (or run turn first to cache lastExecutionId)");
  }
  const uid = requireUserId();
  requireToken();
  const live = env("AVA_ENABLE_LIVE", "") === "true";
  const result = await mcpCall("ava_approve_execute", {
    executionId: id,
    userId: uid,
    portal: portal(),
    mode: live ? "mainnet" : "testnet",
  });
  printJson(result);
}

async function cmdPortfolio() {
  const uid = requireUserId();
  requireToken();
  printJson(
    await mcpCall("ava_portfolio", {
      userId: uid,
      portal: portal(),
    }),
  );
}

async function cmdPrice(asset) {
  if (!asset) fail("Usage: ava price USDC");
  printJson(
    await mcpCall("ava_get_price", {
      asset,
      vsCurrency: "usd",
    }),
  );
}

async function cmdCall(tool, jsonArgs) {
  if (!tool) fail("Usage: ava call <toolName> '<json args>'");
  let args = {};
  if (jsonArgs) {
    try {
      args = JSON.parse(jsonArgs);
    } catch (e) {
      fail(`Invalid JSON args: ${e.message}`);
    }
  }
  printJson(await mcpCall(tool, args));
}

async function cmdHealth() {
  try {
    const h = await http("GET", "/health", { auth: false });
    printJson({ ok: true, base: baseUrl(), health: h });
  } catch (e) {
    printJson({
      ok: false,
      base: baseUrl(),
      error: e.message,
      note: "Start api-worker: pnpm --filter @ava/api-worker dev (or your local start command)",
    });
    process.exit(1);
  }
}

function help() {
  console.log(`Ava OpenClaw CLI: live lend first, copilot is testnet-only

Env:
  AVA_API_BASE   default https://api.getava.xyz (set http://127.0.0.1:8787 for local dev)
  AVA_USER_ID    optional; else ~/.config/ava-openclaw/state.json
  AVA_TOKEN      bearer session token; else ~/.config/ava-openclaw/state.json
                 (created by \`session\`, sent as Authorization: Bearer, never printed)
  AVA_PORTAL     default base
  AVA_ENABLE_LIVE  set true only when live submit is intentionally enabled

Commands:
  health
  session
  tools
  lend <mandateId> [previewHash]
  turn "<message>"          (testnet only)
  approve [executionId]     (testnet only)
  portfolio
  price <asset>
  call <toolName> '<json>'

Canonical LIVE loop (NEVER skip user confirm):
  1. session
  2. call ava_create_mandate '{"portal":"base","message":"Earn on 500 USDC on Base"}'
  3. lend <mandateId>                 # preview, no previewHash
  4. show preview → wait for yes
  5. lend <mandateId> <previewHash>   # execute
  Copilot turn/approve is testnet-only and is not a rehearsal of lend.
`);
}

const [cmd, ...rest] = process.argv.slice(2);

async function main() {
  switch (cmd) {
    case "health":
      return cmdHealth();
    case "session":
      return cmdSession();
    case "tools":
      return cmdTools();
    case "lend":
      return cmdLend(rest[0], rest[1]);
    case "turn":
      return cmdTurn(rest.join(" "));
    case "approve":
      return cmdApprove(rest[0]);
    case "portfolio":
      return cmdPortfolio();
    case "price":
      return cmdPrice(rest[0]);
    case "call":
      return cmdCall(rest[0], rest.slice(1).join(" "));
    case "help":
    case undefined:
      return help();
    default:
      fail(`Unknown command: ${cmd}\nRun: node scripts/ava.mjs help`);
  }
}

main().catch((e) => {
  console.error(e.message || e);
  process.exit(1);
});
