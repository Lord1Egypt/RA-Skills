#!/usr/bin/env node
/**
 * ClawCall Listener
 * Polls ClawCall for inbound call messages and routes them through
 * the local agent, then returns the reply to the caller.
 *
 * Usage:
 *   node clawcall-listener.js
 *
 * Requires:
 *   CLAWCALL_API_KEY environment variable set
 *
 * Agent mode (pick one):
 *   CLAWCALL_AGENT_URL=http://localhost:5000
 *       POST {CLAWCALL_AGENT_URL}/clawcall/message
 *       Body:    { "call_sid": "...", "message": "..." }
 *       Returns: { "response": "...", "end_call": false }
 *
 *   (default) OpenClaw CLI:
 *       openclaw agent --session-id <call_sid> --message <msg> --json
 *       Hard timeout: 9s — process is killed and a fallback plays if exceeded.
 *
 * Security note:
 *   child_process.spawn is used ONLY to invoke the local OpenClaw CLI.
 *   No other shell commands are executed. Set CLAWCALL_AGENT_URL to use
 *   HTTP mode instead and avoid child_process entirely.
 */

"use strict";

const { spawn, execSync } = require("child_process");
const { URL } = require("url");

const API_KEY   = process.env.CLAWCALL_API_KEY;
const BASE_URL  = (process.env.CLAWCALL_BASE_URL || "https://api.clawcall.online").replace(/\/$/, "");
const AGENT_URL = (process.env.CLAWCALL_AGENT_URL || "").replace(/\/$/, "");

// Hard latency budget for openclaw CLI — must reply before AGENT_RESPONSE_TIMEOUT (12s)
const CLI_TIMEOUT_MS = 9_000;

if (!API_KEY) {
  console.error("[ClawCall] ERROR: CLAWCALL_API_KEY is not set.");
  console.error("[ClawCall] Run:  setx CLAWCALL_API_KEY your-api-key  (Windows)");
  console.error("[ClawCall] or:   export CLAWCALL_API_KEY=your-api-key  (Mac/Linux)");
  process.exit(1);
}

const _parsed   = new URL(BASE_URL);
const _isHttps  = _parsed.protocol === "https:";
const _httpLib  = _isHttps ? require("https") : require("http");
const _hostname = _parsed.hostname;
const _port     = _parsed.port ? parseInt(_parsed.port) : (_isHttps ? 443 : 80);

console.log(`[ClawCall] Connecting to ${BASE_URL}`);
if (AGENT_URL) {
  console.log(`[ClawCall] Agent mode: HTTP → ${AGENT_URL}/clawcall/message`);
} else {
  console.log(`[ClawCall] Agent mode: openclaw CLI (timeout ${CLI_TIMEOUT_MS}ms)`);
}

// ── HTTP helper (ClawCall API) ────────────────────────────────────────────────

function request(method, path, body) {
  return new Promise((resolve, reject) => {
    const data = body ? JSON.stringify(body) : null;
    const req  = _httpLib.request(
      {
        hostname: _hostname,
        port:     _port,
        path,
        method,
        headers: {
          Authorization:  `Bearer ${API_KEY}`,
          "Content-Type": "application/json",
          ...(data ? { "Content-Length": Buffer.byteLength(data) } : {}),
        },
      },
      (res) => {
        let raw = "";
        res.on("data", (chunk) => (raw += chunk));
        res.on("end", () => {
          try { resolve(JSON.parse(raw)); }
          catch { resolve({ ok: false, raw }); }
        });
      }
    );
    req.on("error", reject);
    req.setTimeout(25_000, () => req.destroy(new Error("HTTP timeout")));
    if (data) req.write(data);
    req.end();
  });
}

// ── HTTP helper (local agent webhook) ────────────────────────────────────────

function postToAgent(agentUrl, callSid, message) {
  return new Promise((resolve, reject) => {
    const parsed  = new URL(agentUrl);
    const isHttps = parsed.protocol === "https:";
    const lib     = isHttps ? require("https") : require("http");
    const body    = JSON.stringify({ call_sid: callSid, message });

    const req = lib.request(
      {
        hostname: parsed.hostname,
        port:     parsed.port ? parseInt(parsed.port) : (isHttps ? 443 : 80),
        path:     parsed.pathname.replace(/\/$/, "") + "/clawcall/message",
        method:   "POST",
        headers: {
          "Content-Type":   "application/json",
          "Content-Length": Buffer.byteLength(body),
        },
      },
      (res) => {
        let raw = "";
        res.on("data", (c) => (raw += c));
        res.on("end", () => {
          try { resolve(JSON.parse(raw)); }
          catch { resolve({ response: raw, end_call: false }); }
        });
      }
    );
    req.on("error", reject);
    req.setTimeout(50_000, () => req.destroy(new Error("Agent HTTP timeout")));
    req.write(body);
    req.end();
  });
}

// ── Parse openclaw --json output ──────────────────────────────────────────────

function parseOpenClawOutput(raw) {
  if (!raw) return null;

  const lines = raw.split("\n").filter(Boolean).reverse();
  for (const line of lines) {
    try {
      const parsed = JSON.parse(line);
      const fromPayloads = Array.isArray(parsed.payloads) && parsed.payloads[0] && parsed.payloads[0].text;
      let contentText = parsed.content;
      if (Array.isArray(contentText)) {
        const item = contentText.find((c) => c && c.type === "text" && c.text);
        contentText = item ? item.text : null;
      }
      const reply = fromPayloads
        || parsed.result
        || parsed.reply
        || parsed.text
        || parsed.message
        || contentText;
      if (reply && typeof reply === "string" && reply.trim())
        return { reply: reply.trim(), end_call: !!parsed.end_call };
    } catch { /* not JSON */ }
  }

  const trimmed = raw.trim();
  if (trimmed && !trimmed.startsWith("{") && !trimmed.startsWith("["))
    return { reply: trimmed, end_call: false };

  return null;
}

// ── Kill a spawned process (Windows-safe) ─────────────────────────────────────

function killProcess(proc) {
  try { proc.kill(); } catch {}
  // On Windows, also kill the full process tree so cmd.exe doesn't orphan openclaw
  if (process.platform === "win32" && proc.pid) {
    try {
      execSync(`taskkill /PID ${proc.pid} /T /F`, { timeout: 2_000, stdio: "ignore" });
    } catch {}
  }
}

// ── Agent turn ────────────────────────────────────────────────────────────────

async function runAgentTurn(message, callSid) {
  const t0 = Date.now();

  // ── Mode 1: HTTP webhook agent (CLAWCALL_AGENT_URL set) ──────────────────
  if (AGENT_URL) {
    try {
      const data  = await postToAgent(AGENT_URL, callSid, message);
      const reply = (data.response || data.reply || data.text || "").trim();
      if (reply) return { reply, end_call: !!data.end_call };
      console.error("[ClawCall] Agent returned empty response:", data);
      return { reply: "I had a little trouble with that — could you repeat it?", end_call: false };
    } catch (err) {
      console.error("[ClawCall] Agent webhook error:", err.message);
      return { reply: "I had a little trouble with that — could you repeat it?", end_call: false };
    }
  }

  // ── Mode 2: OpenClaw CLI (async spawn, hard 9s timeout) ──────────────────
  return new Promise((resolve) => {
    let settled = false;
    let stdout  = "";

    function settle(result) {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      console.log(`[ClawCall] agent turn: ${Date.now() - t0}ms  end_call=${result.end_call}`);
      resolve(result);
    }

    // Kill the process after CLI_TIMEOUT_MS — ensures fallback arrives
    // within AGENT_RESPONSE_TIMEOUT (12s) so the caller hears something fast
    const timer = setTimeout(() => {
      console.error(`[ClawCall] openclaw timeout (${CLI_TIMEOUT_MS}ms) — killing process`);
      killProcess(proc);
      settle({ reply: "I had a little trouble with that — could you repeat it?", end_call: false });
    }, CLI_TIMEOUT_MS);

    // On Windows, shell:true is required to resolve openclaw.cmd/.ps1 from PATH.
    // On Mac/Linux, shell:false is sufficient and avoids an extra shell layer.
    const proc = spawn(
      "openclaw",
      ["agent", "--session-id", callSid, "--message", message, "--json"],
      {
        shell:       process.platform === "win32",
        windowsHide: true,
        stdio:       ["pipe", "pipe", "pipe"],
      }
    );

    proc.stdout.on("data", (chunk) => { stdout += chunk; });
    proc.stderr.on("data", () => {});  // suppress noisy openclaw stderr

    proc.on("close", (code) => {
      const parsed = parseOpenClawOutput(stdout.trim());
      if (parsed) return settle(parsed);
      if (code !== 0) console.error(`[ClawCall] openclaw exited ${code}`);
      settle({ reply: "I'm here — could you say that again?", end_call: false });
    });

    proc.on("error", (err) => {
      console.error("[ClawCall] openclaw spawn error:", err.message);
      settle({ reply: "I had a little trouble with that — could you repeat it?", end_call: false });
    });
  });
}

// ── Main loop ─────────────────────────────────────────────────────────────────

async function main() {
  console.log("[ClawCall] Listener started. Waiting for calls...");

  while (true) {
    try {
      const res = await request("GET", "/api/v1/calls/listen?timeout=15");

      if (res.ok && res.timeout) continue;

      if (!res.ok || !res.call_sid) {
        console.error("[ClawCall] Unexpected response:", res);
        await sleep(3_000);
        continue;
      }

      const { call_sid, message } = res;
      console.log(`[ClawCall] ↓ call_sid=${call_sid}  message="${message}"`);

      const t0 = Date.now();
      const { reply, end_call } = await runAgentTurn(message, call_sid);
      console.log(`[ClawCall] ↑ reply="${reply.slice(0, 100)}"  end_call=${end_call}`);

      const postRes = await request("POST", `/api/v1/calls/respond/${call_sid}`, {
        response: reply,
        end_call,
      });

      const ms = Date.now() - t0;
      if (!postRes.ok) {
        console.error(`[ClawCall] Respond error (${ms}ms total):`, postRes);
      } else {
        console.log(`[ClawCall] ✓ responded in ${ms}ms total`);
      }

    } catch (err) {
      console.error("[ClawCall] Loop error:", err.message);
      await sleep(3_000);
    }
  }
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

main();
