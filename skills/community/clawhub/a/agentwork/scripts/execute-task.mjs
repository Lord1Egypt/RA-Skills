#!/usr/bin/env node
// execute-task.mjs
// Unified AgentWork task runner:
// claim -> start-execution -> heartbeat -> dispatch -> submit -> release-claim(on failure)

import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { spawn, execFileSync } from "node:child_process";
import { randomUUID, createHash } from "node:crypto";

const DEFAULT_BASE_URL = process.env.AGENTWORK_BASE_URL?.trim() || "https://agentwork.one";
const DEFAULT_AGENT_ID = process.env.AGENTWORK_AGENT_ID?.trim() || process.env.OPENCLAW_AGENT_ID?.trim() || "main";
const DEFAULT_HEARTBEAT_INTERVAL_SEC = 60;
const DEFAULT_MAX_EXECUTION_ATTEMPTS = 2;
const TOKEN_SUBMIT_BUFFER_SEC = 120;
const MIN_TOKEN_SUBMIT_WINDOW_SEC = 30;
const DEFAULT_DISPATCH_TIMEOUT_BY_PROVIDER = {
  openai: 900,
  anthropic: 900,
  manus: 1800,
};
const COMPLEXITY_FACTOR = {
  low: 0.8,
  medium: 1.0,
  high: 1.35,
};
const PROVIDER_REQUIRED_ENV = {
  manus: "MANUS_API_KEY",
};
const PROVIDER_CLI_REQUIREMENT = {
  openai: "codex",
  anthropic: "claude",
};

class ApiError extends Error {
  constructor(input) {
    super(input.message || "API error");
    this.name = "ApiError";
    this.status = input.status;
    this.code = input.code;
    this.details = input.details;
    this.body = input.body;
  }
}

function usage() {
  process.stderr.write(
    [
      "Usage:",
      "  node execute-task.mjs --order-id <ord_xxx> [--provider <openai|anthropic|manus>] [--prompt <text>]",
      "    [--model <model>] [--dispatch-timeout-seconds <sec>]",
      "    [--ttl-seconds <sec>] [--complexity <low|medium|high>] [--max-execution-attempts <n>]",
      "    [--heartbeat-interval-seconds <sec>] [--agent-id <id>] [--state-dir <path>]",
      "    [--api-key <sk_xxx>] [--base-url <https://agentwork.one>] [--keep-state-on-success]",
      "",
      "Environment:",
      "  AGENTWORK_API_KEY (required unless --api-key is provided)",
      "  AGENTWORK_BASE_URL (optional, default: https://agentwork.one)",
      "  AGENTWORK_STATE_DIR (optional, default: ~/.agentwork; legacy OPENCLAW_STATE_DIR also supported)",
      "  AGENTWORK_AGENT_ID (optional, default: main; legacy OPENCLAW_AGENT_ID also supported)",
    ].join("\n"),
  );
}

function outputJson(payload) {
  process.stdout.write(`${JSON.stringify(payload)}\n`);
}

function fatal(payload, exitCode = 1) {
  outputJson({
    ok: false,
    ...payload,
  });
  process.exit(exitCode);
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const raw = argv[i];
    if (!raw.startsWith("--")) continue;
    const key = raw.slice(2);
    const next = argv[i + 1];
    if (next && !next.startsWith("--")) {
      args[key] = next;
      i += 1;
    } else {
      args[key] = true;
    }
  }
  return args;
}

function toInt(value, fallback) {
  const parsed = Number.parseInt(String(value ?? ""), 10);
  if (!Number.isFinite(parsed)) return fallback;
  return parsed;
}

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value));
}

function ensureObject(value) {
  return value && typeof value === "object" && !Array.isArray(value) ? value : {};
}

function resolveHomeDir() {
  const home = process.env.HOME?.trim() || os.homedir?.();
  if (!home) {
    fatal({
      error_code: "MISSING_HOME",
      message: "Cannot resolve HOME for runtime state directory",
      retryable: false,
    });
  }
  return home;
}

function resolveStateRoot(args) {
  if (typeof args["state-dir"] === "string" && args["state-dir"].trim()) {
    return path.resolve(args["state-dir"].trim());
  }
  const envDir = process.env.AGENTWORK_STATE_DIR?.trim() || process.env.OPENCLAW_STATE_DIR?.trim();
  if (envDir) return path.resolve(envDir);
  return path.join(resolveHomeDir(), ".agentwork");
}

function resolveRuntimeDir(args) {
  const stateRoot = resolveStateRoot(args);
  const agentId = String(args["agent-id"] || DEFAULT_AGENT_ID).trim() || "main";
  return {
    stateRoot,
    agentId,
    runtimeDir: path.join(stateRoot, "agents", agentId, "agent", "runtime", "agentwork"),
  };
}

async function ensureRuntimeDir(dirPath) {
  await fs.promises.mkdir(dirPath, { recursive: true, mode: 0o700 });
  try {
    await fs.promises.chmod(dirPath, 0o700);
  } catch {
    // best effort
  }
}

function sanitizeOrderId(orderId) {
  return orderId.replace(/[^a-zA-Z0-9._-]/g, "_");
}

async function readJsonIfExists(filePath) {
  try {
    const raw = await fs.promises.readFile(filePath, "utf8");
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

async function writeJsonAtomic(filePath, payload) {
  const dir = path.dirname(filePath);
  await ensureRuntimeDir(dir);
  const tempPath = `${filePath}.${process.pid}.${randomUUID()}.tmp`;
  const json = `${JSON.stringify(payload, null, 2)}\n`;
  await fs.promises.writeFile(tempPath, json, { encoding: "utf8", mode: 0o600 });
  try {
    await fs.promises.rename(tempPath, filePath);
  } catch {
    await fs.promises.copyFile(tempPath, filePath);
    await fs.promises.unlink(tempPath).catch(() => {});
  }
  try {
    await fs.promises.chmod(filePath, 0o600);
  } catch {
    // best effort
  }
}

function nowIso() {
  return new Date().toISOString();
}

function compactString(value) {
  if (typeof value !== "string") return "";
  return value.trim();
}

function getPath(obj, dottedPath) {
  const keys = dottedPath.split(".");
  let current = obj;
  for (const key of keys) {
    if (!current || typeof current !== "object" || Array.isArray(current) || !(key in current)) {
      return undefined;
    }
    current = current[key];
  }
  return current;
}

function extractPromptFromOrder(order) {
  const candidates = [
    "input.prompt",
    "input.text",
    "buy_request_snapshot.input.prompt",
    "buy_request_snapshot.input.text",
    "sell_listing_snapshot.payload.task.input.prompt",
    "sell_listing_snapshot.payload.task.input.text",
    "sell_listing_snapshot.task.input.prompt",
    "sell_listing_snapshot.task.input.text",
  ];

  for (const key of candidates) {
    const value = getPath(order, key);
    if (typeof value === "string" && value.trim()) {
      return value.trim();
    }
  }
  return "";
}

function buildPromptFromOrder(order, explicitPrompt) {
  const basePrompt = compactString(explicitPrompt) || extractPromptFromOrder(order);
  if (!basePrompt) return "";

  const input = ensureObject(order.input);
  const extras = [];
  const mappings = [
    ["repo_url", "Repo URL"],
    ["language", "Language"],
    ["constraints", "Constraints"],
    ["acceptance_criteria", "Acceptance Criteria"],
  ];
  for (const [field, label] of mappings) {
    const value = input[field];
    if (typeof value === "string" && value.trim()) {
      extras.push(`${label}: ${value.trim()}`);
    } else if (Array.isArray(value) && value.length > 0) {
      extras.push(`${label}: ${value.map((item) => String(item)).join(", ")}`);
    }
  }

  if (extras.length === 0) return basePrompt;
  return `${basePrompt}\n\n${extras.join("\n")}`;
}

function inferComplexity(order, prompt, explicitComplexity) {
  const normalized = compactString(explicitComplexity).toLowerCase();
  if (normalized === "low" || normalized === "medium" || normalized === "high") return normalized;

  let score = 0;
  const promptLen = prompt.length;
  if (promptLen >= 6000) score += 2;
  else if (promptLen >= 1500) score += 1;

  const amountRaw = getPath(order, "pricing.amount_minor");
  const amount = Number.parseInt(String(amountRaw ?? "0"), 10);
  if (Number.isFinite(amount) && amount > 0) {
    if (amount >= 8_000_000) score += 2;
    else if (amount >= 2_000_000) score += 1;
  }

  if (score >= 3) return "high";
  if (score >= 1) return "medium";
  return "low";
}

function computeTimeoutPolicy(input) {
  const provider = input.provider;
  const base = DEFAULT_DISPATCH_TIMEOUT_BY_PROVIDER[provider] ?? 1200;
  const complexityFactor = COMPLEXITY_FACTOR[input.complexity] ?? 1.0;

  let dispatchTimeoutSec = toInt(input.dispatchTimeoutSecArg, 0);
  if (dispatchTimeoutSec <= 0) {
    dispatchTimeoutSec = clamp(Math.round(base * complexityFactor), 600, 2400);
  } else {
    dispatchTimeoutSec = clamp(dispatchTimeoutSec, 60, 3600);
  }

  let ttlSeconds = toInt(input.ttlSecondsArg, 0);
  if (ttlSeconds <= 0) {
    ttlSeconds = clamp(dispatchTimeoutSec + TOKEN_SUBMIT_BUFFER_SEC, 300, 3600);
  } else {
    ttlSeconds = clamp(ttlSeconds, 60, 3600);
  }

  const maxExecutionRaw = getPath(input.order, "deadlines.max_execution_timeout");
  if (typeof maxExecutionRaw === "string") {
    const remainingMs = Date.parse(maxExecutionRaw) - Date.now();
    const remainingSec = Math.floor(remainingMs / 1000);
    if (Number.isFinite(remainingSec) && remainingSec > 0) {
      if (remainingSec <= 180) {
        return {
          ok: false,
          error_code: "ORDER_MAX_EXECUTION_NEAR_DEADLINE",
          message: `max_execution_timeout is too close (${remainingSec}s remaining)`,
          retryable: true,
          remaining_sec: remainingSec,
        };
      }
      ttlSeconds = Math.min(ttlSeconds, Math.max(60, remainingSec - 60));
      dispatchTimeoutSec = Math.min(dispatchTimeoutSec, Math.max(60, ttlSeconds - TOKEN_SUBMIT_BUFFER_SEC));
    }
  }

  return {
    ok: true,
    dispatch_timeout_sec: dispatchTimeoutSec,
    ttl_seconds: ttlSeconds,
  };
}

function extractApiError(payload, status) {
  const obj = ensureObject(payload);
  const nested = ensureObject(obj.error);
  const code = compactString(nested.code) || compactString(obj.code) || `HTTP_${status}`;
  const message =
    compactString(nested.message)
    || compactString(obj.message)
    || `HTTP ${status}`;
  const details = nested.details ?? obj.details ?? null;
  return { code, message, details };
}

async function apiCall(ctx, method, endpointPath, body, timeoutMs = 30000) {
  const url = new URL(endpointPath, ctx.baseUrl).toString();
  const headers = {
    Authorization: `Bearer ${ctx.apiKey}`,
    Accept: "application/json",
  };
  let payload;
  if (body !== undefined) {
    headers["Content-Type"] = "application/json";
    payload = JSON.stringify(body);
  }
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  let response;
  let text = "";
  let parsed = null;
  try {
    response = await fetch(url, {
      method,
      headers,
      body: payload,
      signal: controller.signal,
    });
    text = await response.text();
    if (text.trim()) {
      try {
        parsed = JSON.parse(text);
      } catch {
        parsed = null;
      }
    }
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    throw new ApiError({
      status: 0,
      code: "NETWORK_ERROR",
      message: `Network error calling ${method} ${endpointPath}: ${message}`,
      details: null,
      body: null,
    });
  } finally {
    clearTimeout(timer);
  }

  if (!response.ok) {
    const apiErr = extractApiError(parsed, response.status);
    throw new ApiError({
      status: response.status,
      code: apiErr.code,
      message: apiErr.message,
      details: apiErr.details,
      body: parsed,
    });
  }

  const data = ensureObject(parsed).data;
  return data === undefined ? parsed : data;
}

function normalizeOrderFromAny(payload) {
  const obj = ensureObject(payload);
  const order = ensureObject(obj.order);
  if (Object.keys(order).length > 0) return order;
  return obj;
}

async function runCommandWithTimeout(input) {
  return await new Promise((resolve) => {
    const child = spawn(input.command, input.args, {
      cwd: input.cwd,
      env: input.env,
      stdio: ["ignore", "pipe", "pipe"],
      shell: false,
    });

    let stdout = "";
    let stderr = "";
    let timedOut = false;
    let killed = false;
    const started = Date.now();

    child.stdout.on("data", (chunk) => {
      stdout += chunk.toString();
    });
    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString();
    });

    let killTimer = null;
    let hardKillTimer = null;
    if (input.timeoutMs > 0) {
      killTimer = setTimeout(() => {
        timedOut = true;
        child.kill("SIGTERM");
        hardKillTimer = setTimeout(() => {
          if (!killed) {
            child.kill("SIGKILL");
          }
        }, 5000);
      }, input.timeoutMs);
    }

    child.on("close", (code, signal) => {
      killed = true;
      if (killTimer) clearTimeout(killTimer);
      if (hardKillTimer) clearTimeout(hardKillTimer);
      resolve({
        code: code ?? null,
        signal: signal ?? null,
        stdout,
        stderr,
        timedOut,
        duration_ms: Date.now() - started,
      });
    });
  });
}

function buildSubmitContent(dispatchJson) {
  const content = {};
  if (typeof dispatchJson.output === "string" && dispatchJson.output.trim()) {
    content.text = dispatchJson.output;
  }
  if (dispatchJson.output && typeof dispatchJson.output === "object" && !Array.isArray(dispatchJson.output)) {
    content.json = dispatchJson.output;
  }
  const shareUrl = compactString(dispatchJson.share_url);
  if (shareUrl) {
    content.file_urls = [shareUrl];
  }

  const allowedKeys = new Set(["text", "json", "file_urls"]);
  const keys = Object.keys(content);
  for (const key of keys) {
    if (!allowedKeys.has(key)) {
      throw new Error(`submit content contains unsupported key: ${key}`);
    }
  }
  const hasOutput =
    (typeof content.text === "string" && content.text.trim().length > 0)
    || content.json !== undefined
    || (Array.isArray(content.file_urls) && content.file_urls.length > 0);
  if (!hasOutput) {
    throw new Error("dispatch result did not produce submit content");
  }
  return content;
}

function sanitizeProcessEvidence(processEvidence) {
  const pe = ensureObject(processEvidence);
  const required = [
    "schema_version",
    "provider",
    "tool",
    "run_id",
    "nonce_echo",
    "execution_payload_hash",
    "raw_trace",
    "raw_trace_format",
    "raw_trace_hash",
  ];
  for (const key of required) {
    if (!compactString(pe[key])) {
      throw new Error(`process_evidence.${key} is required`);
    }
  }
  const out = {
    schema_version: String(pe.schema_version),
    provider: String(pe.provider),
    tool: String(pe.tool),
    run_id: String(pe.run_id),
    nonce_echo: String(pe.nonce_echo),
    execution_payload_hash: String(pe.execution_payload_hash),
    raw_trace: String(pe.raw_trace),
    raw_trace_format: String(pe.raw_trace_format),
    raw_trace_hash: String(pe.raw_trace_hash),
  };
  if (pe.provider_evidence && typeof pe.provider_evidence === "object" && !Array.isArray(pe.provider_evidence)) {
    out.provider_evidence = pe.provider_evidence;
  }
  return out;
}

function checkProviderCli(provider) {
  const cli = PROVIDER_CLI_REQUIREMENT[provider];
  if (!cli) return;
  try {
    execFileSync("which", [cli], { stdio: "pipe" });
  } catch {
    fatal({
      error_code: "MISSING_PROVIDER_CLI",
      message: `Provider CLI not found in PATH: ${cli}. Install it and retry.`,
      retryable: false,
    });
  }
}

async function apiCallRaw(url, options) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), options.timeoutMs || 30000);
  try {
    const resp = await fetch(url, {
      method: options.method || "GET",
      headers: options.headers || {},
      body: options.body || undefined,
      signal: controller.signal,
    });
    clearTimeout(timeoutId);
    const text = await resp.text();
    try { return JSON.parse(text); } catch { return { raw: text }; }
  } catch {
    clearTimeout(timeoutId);
    return null;
  }
}

function parseJsonlEvents(rawTrace) {
  return rawTrace.split("\n").filter(Boolean).map(line => {
    try { return JSON.parse(line); } catch { return null; }
  }).filter(Boolean);
}

async function dispatchCodex(input) {
  const model = input.model || "o4-mini";
  const cmdArgs = ["exec", input.prompt, "--json", "--color", "never", "--sandbox", "read-only", "--skip-git-repo-check", "--model", model];
  const startedAt = new Date().toISOString();
  const startEpoch = Date.now();

  const runResult = await runCommandWithTimeout({
    command: "codex",
    args: cmdArgs,
    cwd: process.cwd(),
    env: process.env,
    timeoutMs: input.dispatchTimeoutSec * 1000,
  });

  const completedAt = new Date().toISOString();
  const executionDurationSeconds = Math.floor((Date.now() - startEpoch) / 1000);
  const rawTrace = runResult.stdout || "";
  const rawTraceHash = createHash("sha256").update(rawTrace).digest("hex");
  const events = parseJsonlEvents(rawTrace);

  let runId = "unknown-thread";
  for (const ev of events) {
    if (ev.type === "thread.started" && (ev.thread_id || ev.thread?.id)) {
      runId = ev.thread_id || ev.thread.id;
      break;
    }
  }
  if (runId === "unknown-thread") {
    for (const ev of events) {
      if (ev.thread_id) { runId = ev.thread_id; break; }
    }
  }

  let inputTokens = 0, outputTokens = 0, cachedInputTokens = 0;
  const actionTypes = new Set();
  for (const ev of events) {
    if (ev.type === "turn.completed" && ev.usage) {
      inputTokens += ev.usage.input_tokens || ev.usage.input || 0;
      outputTokens += ev.usage.output_tokens || ev.usage.output || 0;
      cachedInputTokens += ev.usage.cached_input_tokens || ev.usage.cached_input || 0;
    }
    if (ev.type === "item.completed") {
      const at = ev.item?.type || ev.item_type || ev.action_type;
      if (at) actionTypes.add(at);
    }
  }

  let outputText = "";
  for (const ev of events) {
    const val = ev.result || ev.output || ev.message || ev.text || ev.content;
    if (typeof val === "string") outputText = val;
  }

  if (runResult.timedOut) {
    return {
      status: "error",
      error_code: "DISPATCH_TIMEOUT",
      error: "codex timed out",
      run_id: runId,
    };
  }

  const isSuccess = runResult.code === 0;
  return {
    status: isSuccess ? "success" : "error",
    output: outputText,
    run_id: runId,
    started_at: startedAt,
    completed_at: completedAt,
    exit_code: runResult.code,
    stderr: runResult.stderr || "",
    process_evidence: {
      schema_version: "1.0",
      provider: "openai",
      tool: "codex",
      run_id: runId,
      nonce_echo: input.nonce,
      execution_payload_hash: input.executionPayloadHash,
      raw_trace: rawTrace,
      raw_trace_format: "jsonl",
      raw_trace_hash: rawTraceHash,
      provider_evidence: {
        input_tokens: inputTokens,
        output_tokens: outputTokens,
        cached_input_tokens: cachedInputTokens,
        action_types: [...actionTypes],
        event_count: events.length,
        execution_duration_seconds: executionDurationSeconds,
      },
    },
  };
}

async function dispatchClaudeCode(input) {
  const model = input.model || "sonnet";
  const maxBudget = "1.00";
  const cmdArgs = ["-p", input.prompt, "--output-format", "stream-json", "--model", model, "--max-budget-usd", maxBudget, "--no-session-persistence"];
  const permissionMode = process.env.CLAUDE_PERMISSION_MODE;
  if (permissionMode) {
    cmdArgs.push("--permission-mode", permissionMode);
  }

  const startedAt = new Date().toISOString();

  const runResult = await runCommandWithTimeout({
    command: "claude",
    args: cmdArgs,
    cwd: process.cwd(),
    env: process.env,
    timeoutMs: input.dispatchTimeoutSec * 1000,
  });

  const completedAt = new Date().toISOString();
  const rawTrace = runResult.stdout || "";
  const rawTraceHash = createHash("sha256").update(rawTrace).digest("hex");
  const events = parseJsonlEvents(rawTrace);

  let sessionId = "unknown-session";
  for (const ev of events) {
    const sid = ev.session_id || ev.result?.session_id;
    if (sid) { sessionId = sid; break; }
  }

  let outputText = "";
  for (const ev of events) {
    const val = ev.result || ev.message || ev.text;
    if (typeof val === "string") outputText = val;
  }

  let totalCostUsd = 0, numTurns = 0, durationMs = 0, durationApiMs = 0, isError = false, subtype = "unknown";
  for (const ev of events) {
    if (ev.total_cost_usd !== undefined) totalCostUsd = ev.total_cost_usd;
    if (ev.num_turns !== undefined) numTurns = ev.num_turns;
    if (ev.duration_ms !== undefined) durationMs = ev.duration_ms;
    if (ev.duration_api_ms !== undefined) durationApiMs = ev.duration_api_ms;
    if (ev.is_error !== undefined) isError = ev.is_error;
    if (ev.subtype !== undefined) subtype = ev.subtype;
  }

  if (runResult.timedOut) {
    return {
      status: "error",
      error_code: "DISPATCH_TIMEOUT",
      error: "claude timed out",
      run_id: sessionId,
    };
  }

  const isSuccess = runResult.code === 0 && !isError;
  return {
    status: isSuccess ? "success" : "error",
    output: outputText,
    run_id: sessionId,
    started_at: startedAt,
    completed_at: completedAt,
    exit_code: runResult.code,
    stderr: runResult.stderr || "",
    process_evidence: {
      schema_version: "1.0",
      provider: "anthropic",
      tool: "claude_code",
      run_id: sessionId,
      nonce_echo: input.nonce,
      execution_payload_hash: input.executionPayloadHash,
      raw_trace: rawTrace,
      raw_trace_format: "jsonl",
      raw_trace_hash: rawTraceHash,
      provider_evidence: {
        total_cost_usd: totalCostUsd,
        num_turns: numTurns,
        duration_ms: durationMs,
        duration_api_ms: durationApiMs,
        subtype,
        is_error: isError,
      },
    },
  };
}

async function dispatchManusApi(input) {
  const apiKey = process.env.MANUS_API_KEY;
  const baseUrl = (process.env.MANUS_API_BASE_URL || "https://api.manus.ai").replace(/\/+$/, "");
  const model = input.model || process.env.MANUS_MODEL || "";

  const startedAt = new Date().toISOString();
  const startEpoch = Date.now();

  let taskId = "";
  let resumedFromTaskId = "";

  if (input.resumeTaskId) {
    taskId = input.resumeTaskId;
    resumedFromTaskId = input.resumeTaskId;
  } else {
    const promptWithNonce = `${input.prompt}\n\n[audit_ref:${input.nonce}]`;
    const createPayload = model
      ? { prompt: promptWithNonce, model, createShareableLink: true }
      : { prompt: promptWithNonce, createShareableLink: true };

    const createResp = await apiCallRaw(`${baseUrl}/v1/tasks`, {
      method: "POST",
      headers: { "API_KEY": apiKey, "Content-Type": "application/json" },
      body: JSON.stringify(createPayload),
      timeoutMs: 30000,
    });

    taskId = createResp?.task_id || createResp?.id || "";
    if (!taskId) {
      return {
        status: "error",
        error_code: "DISPATCH_CREATE_FAILED",
        error: "failed to create manus task",
      };
    }
  }

  const timeout = input.dispatchTimeoutSec;
  let elapsed = 0;
  let pollInterval = 10;
  let finalResp = null;

  while (elapsed < timeout) {
    const statusResp = await apiCallRaw(`${baseUrl}/v1/tasks/${taskId}`, {
      method: "GET",
      headers: { "API_KEY": apiKey },
      timeoutMs: 15000,
    });

    const taskStatus = statusResp?.status || "";
    if (taskStatus === "completed" || taskStatus === "done") { finalResp = statusResp; break; }
    if (taskStatus === "error" || taskStatus === "failed") { finalResp = statusResp; break; }

    if (elapsed >= 120) pollInterval = 30;
    await new Promise(resolve => setTimeout(resolve, pollInterval * 1000));
    elapsed += pollInterval;
  }

  const completedAt = new Date().toISOString();
  const executionDurationSeconds = Math.floor((Date.now() - startEpoch) / 1000);

  if (!finalResp) {
    return {
      status: "error",
      error_code: "DISPATCH_TIMEOUT",
      error: "task timed out",
      run_id: taskId,
      task_id: taskId,
    };
  }

  const rawTrace = JSON.stringify(finalResp);
  const rawTraceHash = createHash("sha256").update(rawTrace).digest("hex");
  const taskStatus = finalResp.status || "unknown";
  const outputText = finalResp.output || finalResp.result || finalResp.message || "";
  const creditUsage = finalResp.credit_usage || finalResp.credits_used || 0;
  const taskUrl = finalResp.metadata?.task_url || finalResp.task_url || "";
  let shareUrl = finalResp.share_url || finalResp.metadata?.share_url || "";
  const modelUsed = finalResp.model || finalResp.metadata?.model || "";
  const instructions = finalResp.instructions || finalResp.prompt || "";
  const createdTs = finalResp.created_at || 0;
  const updatedTs = finalResp.updated_at || 0;

  const isSuccess = taskStatus === "completed" || taskStatus === "done";

  if (isSuccess && !shareUrl) {
    try {
      const enableResp = await apiCallRaw(`${baseUrl}/v1/tasks/${taskId}`, {
        method: "PUT",
        headers: { "API_KEY": apiKey, "Content-Type": "application/json" },
        body: JSON.stringify({ enableShared: true }),
        timeoutMs: 15000,
      });
      shareUrl = enableResp?.share_url || enableResp?.metadata?.share_url || "";
    } catch { /* best effort */ }
  }

  if (isSuccess && !shareUrl) {
    return {
      status: "error",
      error_code: "MISSING_SHARE_URL",
      error: "task completed but share_url is empty; buyer cannot view results without Manus login",
      run_id: taskId,
      task_id: taskId,
    };
  }

  return {
    status: isSuccess ? "success" : "error",
    error_code: isSuccess ? null : "DISPATCH_TASK_FAILED",
    output: outputText,
    share_url: shareUrl,
    run_id: taskId,
    task_id: taskId,
    resumed_from_task_id: resumedFromTaskId || null,
    started_at: startedAt,
    completed_at: completedAt,
    process_evidence: {
      schema_version: "1.0",
      provider: "manus",
      tool: "manus_api",
      run_id: taskId,
      nonce_echo: input.nonce,
      execution_payload_hash: input.executionPayloadHash,
      raw_trace: rawTrace,
      raw_trace_format: "json",
      raw_trace_hash: rawTraceHash,
      provider_evidence: {
        api_credit_usage: creditUsage,
        task_url: taskUrl,
        share_url: shareUrl,
        resumed_from_task_id: resumedFromTaskId || null,
        model: modelUsed,
        instructions,
        api_created_at: createdTs,
        api_updated_at: updatedTs,
        execution_duration_seconds: executionDurationSeconds,
        task_status: taskStatus,
      },
    },
  };
}

const PROVIDER_DISPATCH_FUNCTION = {
  openai: dispatchCodex,
  anthropic: dispatchClaudeCode,
  manus: dispatchManusApi,
};
const SUPPORTED_PROVIDERS = new Set(Object.keys(PROVIDER_DISPATCH_FUNCTION));

async function runDispatchOnce(input) {
  const dispatchFn = PROVIDER_DISPATCH_FUNCTION[input.provider];
  if (!dispatchFn) {
    return {
      ok: false,
      error_code: "UNSUPPORTED_PROVIDER",
      message: `No dispatch function for provider: ${input.provider}`,
      retryable: false,
    };
  }

  let dispatchResult;
  try {
    dispatchResult = await dispatchFn(input);
  } catch (e) {
    return {
      ok: false,
      error_code: "DISPATCH_FAILED",
      message: `Dispatch threw: ${e.message}`,
      retryable: false,
    };
  }

  const status = compactString(dispatchResult?.status).toLowerCase();
  if (status === "success") {
    return {
      ok: true,
      json: dispatchResult,
      run_result: { code: dispatchResult.exit_code ?? 0, stdout: "", stderr: dispatchResult.stderr || "" },
    };
  }

  const errorCode = compactString(dispatchResult?.error_code) || "DISPATCH_FAILED";
  const message = compactString(dispatchResult?.error) || compactString(dispatchResult?.message) || "dispatch failed";
  const taskId = compactString(dispatchResult?.task_id) || compactString(dispatchResult?.run_id);

  return {
    ok: false,
    error_code: errorCode,
    message,
    task_id: taskId,
    retryable: errorCode === "DISPATCH_TIMEOUT",
    json: dispatchResult,
    run_result: { code: dispatchResult?.exit_code ?? 1, stdout: "", stderr: dispatchResult?.stderr || "" },
  };
}

function startHeartbeatLoop(input) {
  const intervalMs = Math.max(10, input.intervalSec) * 1000;
  let stopped = false;
  let timer = null;

  const tick = async () => {
    if (stopped) return;
    try {
      await apiCall(
        input.client,
        "POST",
        `/agent/v1/orders/${encodeURIComponent(input.orderId)}/heartbeat`,
        {},
        15000,
      );
    } catch {
      // best-effort keepalive
    }
  };

  timer = setInterval(tick, intervalMs);
  timer.unref?.();

  return {
    stop() {
      stopped = true;
      if (timer) clearInterval(timer);
    },
  };
}

function isTokenBindingError(error) {
  if (!(error instanceof ApiError)) return false;
  if (error.code === "CAPACITY_EXECUTION_TOKEN_EXPIRED") return true;
  if (error.code === "VALIDATION_ERROR" && /nonce mismatch|execution_payload_hash mismatch/i.test(error.message)) {
    return true;
  }
  return false;
}

function isRetryableSubmitError(error) {
  if (!(error instanceof ApiError)) return false;
  if (error.status >= 500 && error.status < 600) return true;
  if (error.code === "NETWORK_ERROR") return true;
  return false;
}

async function submitWithRetry(input) {
  const maxAttempts = 2;
  let lastError = null;
  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    try {
      return await apiCall(
        input.client,
        "POST",
        `/agent/v1/orders/${encodeURIComponent(input.orderId)}/submit`,
        input.payload,
        30000,
      );
    } catch (error) {
      lastError = error;
      if (!isRetryableSubmitError(error) || attempt >= maxAttempts) break;
      await new Promise((resolve) => setTimeout(resolve, attempt * 1000));
    }
  }
  throw lastError;
}

async function releaseClaimBestEffort(input) {
  try {
    await apiCall(
      input.client,
      "POST",
      `/agent/v1/orders/${encodeURIComponent(input.orderId)}/release-claim`,
      { reason: input.reason || "execute-task-failure" },
      15000,
    );
    return true;
  } catch {
    return false;
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help || args.h) {
    usage();
    process.exit(0);
  }

  const orderId = compactString(args["order-id"]);
  if (!orderId) {
    usage();
    fatal({
      error_code: "MISSING_ORDER_ID",
      message: "--order-id is required",
      retryable: false,
    });
  }

  const apiKey = compactString(args["api-key"]) || compactString(process.env.AGENTWORK_API_KEY);
  if (!apiKey) {
    fatal({
      error_code: "MISSING_API_KEY",
      message: "AGENTWORK_API_KEY is required (or pass --api-key)",
      retryable: false,
      order_id: orderId,
    });
  }

  const baseUrl = compactString(args["base-url"]) || DEFAULT_BASE_URL;
  const client = { baseUrl, apiKey };

  const { stateRoot, agentId, runtimeDir } = resolveRuntimeDir(args);
  const stateFilePath = path.join(runtimeDir, `${sanitizeOrderId(orderId)}.json`);
  const keepStateOnSuccess = Boolean(args["keep-state-on-success"]);
  const attemptId = compactString(args["attempt-id"]) || randomUUID().slice(0, 8);
  const heartbeatIntervalSec = clamp(
    toInt(args["heartbeat-interval-seconds"], DEFAULT_HEARTBEAT_INTERVAL_SEC),
    15,
    300,
  );
  const maxExecutionAttempts = clamp(
    toInt(args["max-execution-attempts"], DEFAULT_MAX_EXECUTION_ATTEMPTS),
    1,
    3,
  );

  const state = (await readJsonIfExists(stateFilePath)) ?? {};
  const baseState = {
    ...state,
    order_id: orderId,
    agent_id: agentId,
    attempt_id: attemptId,
    state_root: stateRoot,
    started_at: state.started_at || nowIso(),
    updated_at: nowIso(),
    phase: "init",
  };
  await writeJsonAtomic(stateFilePath, baseState);

  let orderData;
  try {
    const orderResp = await apiCall(client, "GET", `/agent/v1/orders/${encodeURIComponent(orderId)}`, undefined, 20000);
    orderData = normalizeOrderFromAny(orderResp);
  } catch (error) {
    fatal({
      error_code: error instanceof ApiError ? error.code : "ORDER_FETCH_FAILED",
      message: error instanceof Error ? error.message : String(error),
      retryable: true,
      order_id: orderId,
    });
  }

  const provider = compactString(args.provider || orderData.provider).toLowerCase();
  if (!SUPPORTED_PROVIDERS.has(provider)) {
    fatal({
      error_code: "UNSUPPORTED_PROVIDER",
      message: `Provider "${provider || "unknown"}" is not supported by execute-task.mjs`,
      retryable: false,
      order_id: orderId,
    });
  }

  const prompt = buildPromptFromOrder(orderData, args.prompt);
  if (!prompt) {
    fatal({
      error_code: "PROMPT_MISSING",
      message: "No prompt found in order snapshots/input; pass --prompt explicitly",
      retryable: false,
      order_id: orderId,
    });
  }

  const complexity = inferComplexity(orderData, prompt, args.complexity);
  const timeoutPlan = computeTimeoutPolicy({
    provider,
    complexity,
    dispatchTimeoutSecArg: args["dispatch-timeout-seconds"],
    ttlSecondsArg: args["ttl-seconds"],
    order: orderData,
  });
  if (!timeoutPlan.ok) {
    const released = await releaseClaimBestEffort({
      client,
      orderId,
      reason: timeoutPlan.error_code,
    });
    fatal({
      error_code: timeoutPlan.error_code,
      message: timeoutPlan.message,
      retryable: timeoutPlan.retryable,
      released_claim: released,
      order_id: orderId,
    });
  }

  checkProviderCli(provider);

  const requiredEnvKey = PROVIDER_REQUIRED_ENV[provider];
  if (requiredEnvKey && !process.env[requiredEnvKey]) {
    fatal({
      error_code: "MISSING_PROVIDER_CREDENTIAL",
      message: `Missing ${requiredEnvKey}. Persist it in your environment or secret store (OpenClaw: openclaw config set env.vars.${requiredEnvKey} "<your-key>")`,
      retryable: false,
      order_id: orderId,
    });
  }

  let claimOwned = false;
  try {
    await writeJsonAtomic(stateFilePath, {
      ...baseState,
      phase: "claiming",
      provider,
      prompt_length: prompt.length,
      complexity,
      dispatch_timeout_sec: timeoutPlan.dispatch_timeout_sec,
      ttl_seconds: timeoutPlan.ttl_seconds,
      updated_at: nowIso(),
    });

    try {
      const claimResp = await apiCall(
        client,
        "POST",
        `/agent/v1/orders/${encodeURIComponent(orderId)}/claim`,
        {},
        20000,
      );
      const orderFromClaim = normalizeOrderFromAny(claimResp);
      if (Object.keys(orderFromClaim).length > 0) {
        orderData = orderFromClaim;
      }
      claimOwned = true;
    } catch (error) {
      if (error instanceof ApiError && error.code === "ORDER_INVALID_STATE") {
        // Continue for restart scenarios where order is already claimed or was reclaimed elsewhere.
        claimOwned = true;
      } else {
        throw error;
      }
    }

    let finalSubmit = null;
    let finalDispatch = null;
    let persistedManusTaskId = provider === "manus"
      ? compactString(getPath(state, "dispatch.manus_task_id"))
      : "";

    for (let executionAttempt = 1; executionAttempt <= maxExecutionAttempts; executionAttempt += 1) {
      await writeJsonAtomic(stateFilePath, {
        ...baseState,
        phase: "start_execution",
        provider,
        execution_attempt: executionAttempt,
        dispatch_timeout_sec: timeoutPlan.dispatch_timeout_sec,
        ttl_seconds: timeoutPlan.ttl_seconds,
        updated_at: nowIso(),
      });

      const startResp = await apiCall(
        client,
        "POST",
        `/agent/v1/orders/${encodeURIComponent(orderId)}/start-execution`,
        {
          ttl_seconds: timeoutPlan.ttl_seconds,
        },
        20000,
      );

      const executionToken = compactString(startResp.execution_token);
      const nonce = compactString(startResp.nonce);
      const executionPayloadHash = compactString(startResp.execution_payload_hash);
      const expiresAt = compactString(startResp.expires_at);
      if (!executionToken || !nonce || !executionPayloadHash || !expiresAt) {
        throw new Error("start-execution response missing required fields");
      }

      // For Manus we keep the latest successful task_id in runtime state and
      // reuse it across attempts to avoid re-creating expensive tasks.
      //
      // Security note: cross-attempt resume uses a fresh execution token/nonce
      // but can reuse a previously created task trace. Current receipt checks
      // bind nonce/execution_payload_hash at process_evidence level.
      let resumeTaskId = provider === "manus" ? persistedManusTaskId : "";
      let resumedOnce = false;

      const heartbeat = startHeartbeatLoop({
        client,
        orderId,
        intervalSec: heartbeatIntervalSec,
      });

      let dispatchResult;
      try {
        await writeJsonAtomic(stateFilePath, {
          ...baseState,
          phase: "dispatching",
          provider,
          execution_attempt: executionAttempt,
          token_expires_at: expiresAt,
          dispatch: {
            manus_task_id: resumeTaskId || null,
            resumed_once: resumedOnce,
          },
          updated_at: nowIso(),
        });

        dispatchResult = await runDispatchOnce({
          provider,
          prompt,
          nonce,
          executionPayloadHash,
          model: compactString(args.model),
          dispatchTimeoutSec: timeoutPlan.dispatch_timeout_sec,
          resumeTaskId,
        });

        if (!dispatchResult.ok && provider === "manus" && dispatchResult.error_code === "DISPATCH_TIMEOUT") {
          const taskId = compactString(dispatchResult.task_id);
          const remainingSec = Math.floor((Date.parse(expiresAt) - Date.now()) / 1000);
          if (taskId && !resumedOnce && remainingSec > MIN_TOKEN_SUBMIT_WINDOW_SEC) {
            resumedOnce = true;
            resumeTaskId = taskId;
            await writeJsonAtomic(stateFilePath, {
              ...baseState,
              phase: "dispatch_resume",
              provider,
              execution_attempt: executionAttempt,
              token_expires_at: expiresAt,
              dispatch: {
                manus_task_id: resumeTaskId,
                resumed_once: true,
              },
              updated_at: nowIso(),
            });
            dispatchResult = await runDispatchOnce({
              provider,
              prompt,
              nonce,
              executionPayloadHash,
              model: compactString(args.model),
              dispatchTimeoutSec: timeoutPlan.dispatch_timeout_sec,
              resumeTaskId,
            });
          }
        }
      } finally {
        heartbeat.stop();
      }

      if (!dispatchResult.ok) {
        const released = claimOwned
          ? await releaseClaimBestEffort({
              client,
              orderId,
              reason: dispatchResult.error_code,
            })
          : false;
        fatal({
          error_code: dispatchResult.error_code,
          message: dispatchResult.message,
          retryable: dispatchResult.retryable === true,
          released_claim: released,
          order_id: orderId,
          provider,
          execution_attempt: executionAttempt,
          dispatch_task_id: dispatchResult.task_id || null,
        });
      }

      finalDispatch = dispatchResult.json;
      const dispatchTaskId = compactString(finalDispatch.task_id || finalDispatch.run_id);
      const dispatchRunId = compactString(finalDispatch.run_id);
      const dispatchShareUrl = compactString(finalDispatch.share_url);
      if (provider === "manus" && dispatchTaskId) {
        persistedManusTaskId = dispatchTaskId;
      }

      await writeJsonAtomic(stateFilePath, {
        ...baseState,
        phase: "dispatch_succeeded",
        provider,
        execution_attempt: executionAttempt,
        token_expires_at: expiresAt,
        dispatch: {
          run_id: dispatchRunId || null,
          manus_task_id: provider === "manus" ? (dispatchTaskId || null) : null,
          share_url: dispatchShareUrl || null,
          resumed_once: resumedOnce,
        },
        updated_at: nowIso(),
      });

      const tokenRemainingSec = Math.floor((Date.parse(expiresAt) - Date.now()) / 1000);
      if (tokenRemainingSec < MIN_TOKEN_SUBMIT_WINDOW_SEC) {
        if (executionAttempt < maxExecutionAttempts) {
          await writeJsonAtomic(stateFilePath, {
            ...baseState,
            phase: "retry_pending_token_window",
            provider,
            execution_attempt: executionAttempt,
            token_expires_at: expiresAt,
            dispatch: {
              run_id: dispatchRunId || null,
              manus_task_id: provider === "manus" ? (dispatchTaskId || null) : null,
              share_url: dispatchShareUrl || null,
              resumed_once: resumedOnce,
            },
            retry_reason: "TOKEN_WINDOW_EXHAUSTED",
            updated_at: nowIso(),
          });
          continue;
        }
        const released = claimOwned
          ? await releaseClaimBestEffort({
              client,
              orderId,
              reason: "TOKEN_WINDOW_EXHAUSTED",
            })
          : false;
        fatal({
          error_code: "TOKEN_WINDOW_EXHAUSTED",
          message: `execution token too close to expiry before submit (${tokenRemainingSec}s remaining)`,
          retryable: true,
          released_claim: released,
          order_id: orderId,
          provider,
        });
      }

      const submitContent = buildSubmitContent(finalDispatch);
      const processEvidence = sanitizeProcessEvidence(finalDispatch.process_evidence);
      const submitPayload = {
        execution_token: executionToken,
        content: submitContent,
        process_evidence: processEvidence,
        idempotency_key: `sub:${orderId}:${attemptId}:${executionAttempt}`.slice(0, 100),
      };

      await writeJsonAtomic(stateFilePath, {
        ...baseState,
        phase: "submitting",
        provider,
        execution_attempt: executionAttempt,
        dispatch: {
          manus_task_id: compactString(finalDispatch.task_id || finalDispatch.run_id) || null,
          resumed_once: resumedOnce,
        },
        token_expires_at: expiresAt,
        updated_at: nowIso(),
      });

      try {
        finalSubmit = await submitWithRetry({
          client,
          orderId,
          payload: submitPayload,
        });
        break;
      } catch (error) {
        if (isTokenBindingError(error) && executionAttempt < maxExecutionAttempts) {
          await writeJsonAtomic(stateFilePath, {
            ...baseState,
            phase: "retry_pending_token_binding",
            provider,
            execution_attempt: executionAttempt,
            dispatch: {
              run_id: dispatchRunId || null,
              manus_task_id: provider === "manus" ? (dispatchTaskId || null) : null,
              share_url: dispatchShareUrl || null,
              resumed_once: resumedOnce,
            },
            retry_reason: error instanceof ApiError ? error.code : "TOKEN_BINDING_RETRY",
            updated_at: nowIso(),
          });
          continue;
        }
        const released = claimOwned
          ? await releaseClaimBestEffort({
              client,
              orderId,
              reason: error instanceof ApiError ? error.code : "SUBMIT_FAILED",
            })
          : false;
        fatal({
          error_code: error instanceof ApiError ? error.code : "SUBMIT_FAILED",
          message: error instanceof Error ? error.message : String(error),
          retryable: isRetryableSubmitError(error) || isTokenBindingError(error),
          released_claim: released,
          order_id: orderId,
          provider,
          execution_attempt: executionAttempt,
        });
      }
    }

    if (!finalSubmit || !finalDispatch) {
      const released = claimOwned
        ? await releaseClaimBestEffort({
            client,
            orderId,
            reason: "EXECUTION_RETRY_EXHAUSTED",
          })
        : false;
      fatal({
        error_code: "EXECUTION_RETRY_EXHAUSTED",
        message: "execution attempts exhausted",
        retryable: true,
        released_claim: released,
        order_id: orderId,
        provider,
      });
    }

    await writeJsonAtomic(stateFilePath, {
      ...baseState,
      phase: "submitted",
      provider,
      completed_at: nowIso(),
      updated_at: nowIso(),
      dispatch: {
        run_id: compactString(finalDispatch.run_id) || null,
        task_id: compactString(finalDispatch.task_id || finalDispatch.run_id) || null,
        share_url: compactString(finalDispatch.share_url) || null,
      },
      submit_result: finalSubmit,
    });

    if (!keepStateOnSuccess) {
      await fs.promises.unlink(stateFilePath).catch(() => {});
    }

    const orderFromSubmit = normalizeOrderFromAny(finalSubmit.order);
    const submission = ensureObject(finalSubmit.submission);

    outputJson({
      ok: true,
      order_id: orderId,
      provider,
      order_status: orderFromSubmit.status || null,
      submission_id: submission.id || null,
      run_id: compactString(finalDispatch.run_id) || null,
      share_url: compactString(finalDispatch.share_url) || null,
      retryable: false,
      released_claim: false,
    });
  } catch (error) {
    const released = claimOwned
      ? await releaseClaimBestEffort({
          client,
          orderId,
          reason: error instanceof ApiError ? error.code : "EXECUTE_TASK_FAILED",
        })
      : false;
    fatal({
      error_code: error instanceof ApiError ? error.code : "EXECUTE_TASK_FAILED",
      message: error instanceof Error ? error.message : String(error),
      retryable: error instanceof ApiError ? (error.status >= 500 || error.code === "NETWORK_ERROR") : true,
      released_claim: released,
      order_id: orderId,
    });
  }
}

main();
