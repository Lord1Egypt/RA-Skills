import { spawn } from "child_process";
import { homedir } from "os";
import { readFileSync } from "fs";
import { loadJson } from "./persistence.ts";
import { resolve } from "path";
import { extractJSON } from "./utils.ts";
let _consecutiveFailures = 0;
let _circuitBreakerUntil = 0;
const CIRCUIT_BREAKER_THRESHOLD = 3;
const CIRCUIT_BREAKER_COOLDOWN_MS = 36e5;
const CC_SOUL_HOME = resolve(homedir(), ".cc-soul/data");
const AI_CONFIG_PATH = resolve(CC_SOUL_HOME, "ai_config.json");
let _fallbackApiConfig = null;
function detectAIConfig() {
  try {
    const { mkdirSync, existsSync: existsSync2, writeFileSync } = require("fs");
    mkdirSync(CC_SOUL_HOME, { recursive: true });
    if (!existsSync2(AI_CONFIG_PATH)) {
      writeFileSync(AI_CONFIG_PATH, JSON.stringify({
        backend: "openai-compatible",
        api_base: "",
        api_key: "",
        api_model: "",
        _guide: "\u586B\u5199 api_base\u3001api_key\u3001api_model \u4E09\u4E2A\u5B57\u6BB5\u5373\u53EF\u3002",
        _examples: {
          DeepSeek: { api_base: "https://api.deepseek.com/v1", api_model: "deepseek-chat" },
          OpenAI: { api_base: "https://api.openai.com/v1", api_model: "gpt-4o-mini" },
          Ollama: { api_base: "http://localhost:11434/v1", api_key: "ollama", api_model: "qwen2.5:7b" }
        }
      }, null, 2));
      console.log(`[cc-soul][ai] \u5DF2\u521B\u5EFA\u914D\u7F6E\u6A21\u677F: ${AI_CONFIG_PATH}`);
    }
  } catch {
  }
  const userConfig = loadJson(AI_CONFIG_PATH, {});
  if (userConfig.backend && userConfig.api_base && userConfig.api_key) {
    console.log(`[cc-soul][ai] using ai_config.json: ${userConfig.api_model || "unknown"} @ ${userConfig.api_base}`);
    return {
      backend: userConfig.backend,
      cli_command: userConfig.cli_command || "",
      cli_args: userConfig.cli_args || [],
      api_base: userConfig.api_base || "",
      api_key: userConfig.api_key || "",
      api_model: userConfig.api_model || "",
      max_concurrent: userConfig.max_concurrent || 5
    };
  }
  console.log(`[cc-soul][ai] \u672A\u914D\u7F6E LLM\uFF0C\u7EAF NAM \u6A21\u5F0F\u3002\u914D\u7F6E\u65B9\u6CD5\uFF1A\u7F16\u8F91 ${AI_CONFIG_PATH} \u586B\u5165 api_base\u3001api_key\u3001api_model`);
  return {
    backend: "openai-compatible",
    cli_command: "",
    cli_args: [],
    api_base: "",
    api_key: "",
    api_model: "",
    max_concurrent: 5
  };
}
const LLM_PROVIDERS = {
  deepseek: { api_base: "https://api.deepseek.com/v1", default_model: "deepseek-chat", name: "DeepSeek" },
  openai: { api_base: "https://api.openai.com/v1", default_model: "gpt-4o-mini", name: "OpenAI" },
  siliconflow: { api_base: "https://api.siliconflow.cn/v1", default_model: "Qwen/Qwen2.5-7B-Instruct", name: "\u7845\u57FA\u6D41\u52A8" },
  volcengine: { api_base: "https://ark.cn-beijing.volces.com/api/v3", default_model: "", name: "\u706B\u5C71\u5F15\u64CE" },
  ollama: { api_base: "http://localhost:11434/v1", default_model: "qwen2.5:7b", name: "Ollama\uFF08\u672C\u5730\uFF09" }
};
let _llmValidated = null;
async function validateLLM() {
  if (!hasLLM()) return { ok: false, error: "\u672A\u914D\u7F6E LLM" };
  const cfg = _fallbackApiConfig || aiConfig;
  if (!cfg.api_base || !cfg.api_key) return { ok: false, error: "\u672A\u914D\u7F6E api_base \u6216 api_key" };
  try {
    const resp = await fetch(cfg.api_base + "/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${cfg.api_key}`
      },
      body: JSON.stringify({
        model: cfg.api_model,
        messages: [{ role: "user", content: "hi" }],
        max_tokens: 1
      }),
      signal: AbortSignal.timeout(1e4)
    });
    if (resp.ok) {
      _llmValidated = { ok: true, ts: Date.now() };
      return { ok: true };
    }
    const body = await resp.text().catch(() => "");
    let error = `HTTP ${resp.status}`;
    if (resp.status === 401) error = "API Key \u65E0\u6548";
    else if (resp.status === 404) error = "API \u5730\u5740\u9519\u8BEF\u6216\u6A21\u578B\u4E0D\u5B58\u5728";
    else if (body) error += `: ${body.slice(0, 100)}`;
    _llmValidated = { ok: false, error, ts: Date.now() };
    return { ok: false, error };
  } catch (e) {
    const error = e.name === "TimeoutError" ? "API \u8FDE\u63A5\u8D85\u65F6\uFF0810s\uFF09" : `\u8FDE\u63A5\u5931\u8D25: ${e.message}`;
    _llmValidated = { ok: false, error, ts: Date.now() };
    return { ok: false, error };
  }
}
function getLLMStatus() {
  const cfg = _fallbackApiConfig || aiConfig;
  const configured = !!(cfg.api_base && cfg.api_key);
  return {
    configured,
    connected: _llmValidated?.ok ?? false,
    model: cfg.api_model || "",
    error: _llmValidated?.error
  };
}
function saveLLMConfig(api_base, api_key, api_model) {
  const { writeFileSync } = require("fs");
  const config = {
    backend: "openai-compatible",
    api_base,
    api_key,
    api_model,
    max_concurrent: 5
  };
  writeFileSync(AI_CONFIG_PATH, JSON.stringify(config, null, 2));
  aiConfig.backend = "openai-compatible";
  aiConfig.api_base = api_base;
  aiConfig.api_key = api_key;
  aiConfig.api_model = api_model;
  _fallbackApiConfig = { ...aiConfig, cli_command: "", cli_args: [] };
  _llmValidated = null;
  console.log(`[cc-soul][ai] config saved & activated: ${api_model} @ ${api_base}`);
}
function getFallbackApiConfig() {
  return _fallbackApiConfig;
}
function setFallbackApiConfig(config) {
  _fallbackApiConfig = config;
  if (config.api_base && config.api_key && config.api_model) {
    aiConfig.backend = "openai-compatible";
    aiConfig.api_base = config.api_base;
    aiConfig.api_key = config.api_key;
    aiConfig.api_model = config.api_model;
    console.log(`[cc-soul][ai] main config updated: ${config.api_model} @ ${config.api_base}`);
  }
}
let aiConfig = detectAIConfig();
let _configMtime = 0;
try {
  _configMtime = require("fs").statSync(AI_CONFIG_PATH).mtimeMs;
} catch {
}
function loadAIConfig() {
  aiConfig = detectAIConfig();
  try {
    _configMtime = require("fs").statSync(AI_CONFIG_PATH).mtimeMs;
  } catch {
  }
}
function hotReloadIfChanged() {
  try {
    const mtime = require("fs").statSync(AI_CONFIG_PATH).mtimeMs;
    if (mtime > _configMtime) {
      _configMtime = mtime;
      aiConfig = detectAIConfig();
      _llmValidated = null;
      console.log(`[cc-soul][ai] ai_config.json changed, hot-reloaded: ${aiConfig.api_model || "none"}`);
      if (hasLLM()) {
        validateLLM().then((r) => {
          if (r.ok) console.log(`[cc-soul][ai] \u2705 \u8FDE\u63A5\u9A8C\u8BC1\u901A\u8FC7: ${aiConfig.api_model}`);
          else console.log(`[cc-soul][ai] \u274C \u8FDE\u63A5\u9A8C\u8BC1\u5931\u8D25: ${r.error}`);
        }).catch(() => {
        });
      }
    }
  } catch {
  }
}
function getAIConfig() {
  return aiConfig;
}
let activeCLICount = 0;
let agentBusy = false;
function getAgentBusy() {
  return agentBusy;
}
function setAgentBusy(busy) {
  agentBusy = busy;
  if (!busy) drainQueue();
}
let consecutiveFailures = 0;
const MAX_FAILURES_BEFORE_DEGRADE = 1;
let degradedMode = false;
let degradedAt = 0;
const DEGRADE_RECOVERY_MS = 5 * 60 * 1e3;
function isCliDegraded() {
  return degradedMode;
}
function hasLLM() {
  if (isCliDegraded()) return false;
  const cfg = _fallbackApiConfig || aiConfig;
  if (cfg?.backend === "openai-compatible" && cfg.api_base && cfg.api_key) return true;
  if (cfg?.backend === "cli" && cfg.cli_command) return true;
  return false;
}
const taskQueue = [];
const MAX_QUEUE_SIZE = 10;
function drainQueue() {
  while (taskQueue.length > 0 && !agentBusy && activeCLICount < aiConfig.max_concurrent) {
    const task = taskQueue.shift();
    console.log(`[cc-soul][ai] \u961F\u5217\u53D6\u51FA: ${task.label} (\u5269\u4F59 ${taskQueue.length})`);
    executeTask(task.prompt, task.callback, task.timeoutMs, task.label);
  }
}
let onTaskDone = null;
function setOnTaskDone(cb) {
  onTaskDone = cb;
}
const activeTasks = /* @__PURE__ */ new Map();
let taskIdCounter = 0;
function getActiveTaskStatus() {
  if (activeTasks.size === 0 && taskQueue.length === 0) return "";
  const now = Date.now();
  const running = [...activeTasks.values()].map((t) => {
    const elapsed = Math.round((now - t.startedAt) / 1e3);
    const status = t.hasOutput ? "\u2699\uFE0F" : "\u23F3";
    return `${status} ${t.label} (${elapsed}s)`;
  });
  const queued = taskQueue.length > 0 ? [`\u{1F4CB} \u6392\u961F ${taskQueue.length} \u4E2A`] : [];
  return [...running, ...queued].join(" | ");
}
const HARD_TIMEOUT_MS = 3e4;
const _workloadCosts = /* @__PURE__ */ new Map();
function getWorkloadCosts() {
  return Object.fromEntries(_workloadCosts);
}
function trackWorkload(label, estimatedTokens) {
  const workload = label.split(":")[0] || "unknown";
  const entry = _workloadCosts.get(workload) ?? { calls: 0, tokens: 0 };
  entry.calls++;
  entry.tokens += estimatedTokens;
  _workloadCosts.set(workload, entry);
}
function spawnCLI(prompt, callback, timeoutMs = 12e4, label = "ai-task") {
  if (Date.now() < _circuitBreakerUntil) {
    console.log(`[cc-soul][ai] circuit breaker OPEN: ${_consecutiveFailures} consecutive failures, cooldown until ${new Date(_circuitBreakerUntil).toISOString()}`);
    callback("");
    return;
  }
  trackWorkload(label, Math.ceil(prompt.length * 0.8));
  let callbackSettled = false;
  const hardTimer = setTimeout(() => {
    if (!callbackSettled) {
      callbackSettled = true;
      console.log(`[cc-soul][ai] HARD TIMEOUT (${HARD_TIMEOUT_MS}ms) for ${label} \u2014 forcing callback('')`);
      callback("");
    }
  }, HARD_TIMEOUT_MS);
  const safeCallback = (result) => {
    if (callbackSettled) return;
    callbackSettled = true;
    clearTimeout(hardTimer);
    if (result === "") {
      _consecutiveFailures++;
      if (_consecutiveFailures >= CIRCUIT_BREAKER_THRESHOLD) {
        _circuitBreakerUntil = Date.now() + CIRCUIT_BREAKER_COOLDOWN_MS;
        console.log(`[cc-soul][ai] circuit breaker OPEN: ${_consecutiveFailures} consecutive failures, cooldown until ${new Date(_circuitBreakerUntil).toISOString()}`);
      }
    } else {
      _consecutiveFailures = 0;
    }
    callback(result);
  };
  console.log(`[cc-soul][ai] spawnCLI: backend=${aiConfig.backend} fallback=${!!_fallbackApiConfig} label=${label}`);
  if (aiConfig.backend === "cli" && _fallbackApiConfig) {
    callOpenAICompatibleDirect(_fallbackApiConfig, prompt, (result) => {
      if (onTaskDone) onTaskDone(label, 0, result.length > 0);
      safeCallback(result);
    }, timeoutMs);
    return;
  }
  if (activeCLICount >= 1) {
    if (taskQueue.length >= MAX_QUEUE_SIZE) {
      console.log(`[cc-soul][ai] queue full (${MAX_QUEUE_SIZE}), dropping: ${label}`);
      safeCallback("");
      return;
    }
    taskQueue.push({ prompt, callback: safeCallback, timeoutMs, label });
    return;
  }
  executeTask(prompt, safeCallback, timeoutMs, label);
}
function executeTask(prompt, callback, timeoutMs, label) {
  activeCLICount++;
  const taskId = taskIdCounter++;
  const startedAt = Date.now();
  const wrappedCallback = (result) => {
    const elapsed = Math.round((Date.now() - startedAt) / 1e3);
    const success = result.length > 0;
    if (onTaskDone) onTaskDone(label, elapsed, success);
    callback(result);
    setTimeout(() => drainQueue(), 100);
  };
  if (aiConfig.backend === "openai-compatible") {
    activeTasks.set(taskId, { label, startedAt, hasOutput: false });
    callOpenAICompatible(prompt, (result) => {
      activeTasks.delete(taskId);
      wrappedCallback(result);
    }, timeoutMs);
  } else {
    callCLI(prompt, wrappedCallback, timeoutMs, label, taskId);
  }
}
function callCLI(prompt, callback, timeoutMs, label, taskId) {
  activeTasks.set(taskId, { label, startedAt: Date.now(), hasOutput: false });
  let settled = false;
  function release() {
    if (!settled) {
      settled = true;
      activeCLICount--;
      activeTasks.delete(taskId);
    }
  }
  try {
    const proc = spawn(aiConfig.cli_command, [...aiConfig.cli_args, prompt], {
      cwd: homedir(),
      timeout: timeoutMs,
      stdio: ["pipe", "pipe", "pipe"]
    });
    proc.stdin?.end();
    const killTimer = setTimeout(() => {
      if (proc.pid) {
        try {
          process.kill(proc.pid, 0);
          process.kill(proc.pid, "SIGKILL");
          console.log(`[cc-soul][ai] force-killed stuck PID ${proc.pid}`);
        } catch {
        }
      }
    }, timeoutMs + 1e4);
    proc.on("close", () => clearTimeout(killTimer));
    const MAX_OUTPUT = 512 * 1024;
    let output = "";
    proc.stdout?.on("data", (d) => {
      const task = activeTasks.get(taskId);
      if (task) task.hasOutput = true;
      if (output.length < MAX_OUTPUT) {
        output += d.toString();
        if (output.length > MAX_OUTPUT) output = output.slice(0, MAX_OUTPUT);
      }
    });
    proc.stderr?.on("data", () => {
    });
    const heartbeat = setInterval(() => {
      const task = activeTasks.get(taskId);
      const elapsed = task ? Math.round((Date.now() - task.startedAt) / 1e3) : 0;
      console.log(`[cc-soul][ai] ${label}: ${task?.hasOutput ? "\u5DE5\u4F5C\u4E2D" : "\u7B49\u5F85\u4E2D"} (${elapsed}s, ${Math.round(output.length / 1024)}kb)`);
    }, 3e4);
    proc.on("close", (code, signal) => {
      clearInterval(heartbeat);
      const elapsed = Math.round((Date.now() - (activeTasks.get(taskId)?.startedAt || Date.now())) / 1e3);
      release();
      if (signal === "SIGTERM") {
        console.log(`[cc-soul][ai] ${label}: \u8D85\u65F6 (${timeoutMs}ms)`);
        consecutiveFailures++;
        if (consecutiveFailures >= MAX_FAILURES_BEFORE_DEGRADE && !degradedMode) {
          degradedMode = true;
          degradedAt = Date.now();
          console.error("[cc-soul][ai] CLI degraded mode: too many consecutive failures");
        }
        callback("");
        return;
      }
      const trimmed = output.trim();
      const isErrorOutput = /Invalid API key|API key expired|authentication failed|rate limit|overloaded/i.test(trimmed);
      if (isErrorOutput || code !== 0) {
        consecutiveFailures++;
        if (consecutiveFailures >= MAX_FAILURES_BEFORE_DEGRADE && !degradedMode) {
          degradedMode = true;
          degradedAt = Date.now();
          console.error(`[cc-soul][ai] CLI degraded mode: too many failures (last: ${trimmed.slice(0, 80)})`);
        }
        console.log(`[cc-soul][ai] ${label}: CLI \u9519\u8BEF (code=${code}, ${trimmed.slice(0, 80)})`);
        callback("");
        return;
      }
      consecutiveFailures = 0;
      degradedMode = false;
      console.log(`[cc-soul][ai] ${label}: \u5B8C\u6210 (${elapsed}s, ${output.length}bytes)`);
      callback(trimmed);
    });
    proc.on("error", (err) => {
      clearInterval(heartbeat);
      release();
      consecutiveFailures++;
      console.error(`[cc-soul][ai] ${label}: \u9519\u8BEF ${err.message}`);
      callback("");
    });
  } catch (err) {
    release();
    console.error(`[cc-soul][ai] CLI spawn failed: ${err.message}`);
    callback("");
  }
}
function killGatewayClaude() {
}
async function callOpenAICompatible(prompt, callback, timeoutMs) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const resp = await fetch(`${aiConfig.api_base}/chat/completions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${aiConfig.api_key}`
      },
      body: JSON.stringify({
        model: aiConfig.api_model,
        messages: [{ role: "user", content: prompt }],
        max_tokens: 2048
      }),
      signal: controller.signal
    });
    clearTimeout(timer);
    if (!resp.ok) {
      const errText = await resp.text().catch(() => "");
      console.error(`[cc-soul][ai] API error ${resp.status}: ${errText.slice(0, 200)}`);
      consecutiveFailures++;
      if (consecutiveFailures >= MAX_FAILURES_BEFORE_DEGRADE && !degradedMode) {
        degradedMode = true;
        degradedAt = Date.now();
        console.error("[cc-soul][ai] CLI degraded mode: too many consecutive failures");
      }
      callback("");
      return;
    }
    const data = await resp.json();
    const content = data.choices?.[0]?.message?.content || "";
    consecutiveFailures = 0;
    degradedMode = false;
    callback(content.trim());
  } catch (e) {
    clearTimeout(timer);
    consecutiveFailures++;
    if (consecutiveFailures >= MAX_FAILURES_BEFORE_DEGRADE && !degradedMode) {
      degradedMode = true;
      degradedAt = Date.now();
      console.error("[cc-soul][ai] CLI degraded mode: too many consecutive failures");
    }
    if (e.name === "AbortError") {
      console.log(`[cc-soul][ai] API timeout after ${timeoutMs}ms`);
    } else {
      console.error(`[cc-soul][ai] API error: ${e.message}`);
    }
    callback("");
  } finally {
    activeCLICount--;
  }
}
async function callOpenAICompatibleDirect(cfg, prompt, callback, timeoutMs) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const resp = await fetch(`${cfg.api_base}/chat/completions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${cfg.api_key}`
      },
      body: JSON.stringify({
        model: cfg.api_model,
        messages: [{ role: "user", content: prompt }],
        max_tokens: 2048
      }),
      signal: controller.signal
    });
    clearTimeout(timer);
    if (!resp.ok) {
      const errText = await resp.text().catch(() => "");
      console.error(`[cc-soul][ai] fallback API error ${resp.status}: ${errText.slice(0, 200)}`);
      callback("");
      return;
    }
    const data = await resp.json();
    const content = data.choices?.[0]?.message?.content || "";
    console.log(`[cc-soul][ai] fallback API ok: ${content.length} chars`);
    callback(content.trim());
  } catch (e) {
    clearTimeout(timer);
    console.error(`[cc-soul][ai] fallback API error: ${e.message}`);
    callback("");
  }
}
const HAIKU_MODEL = "claude-haiku-4-5-20251001";
let anthropicApiKey = "";
function getAnthropicApiKey() {
  if (anthropicApiKey) return anthropicApiKey;
  try {
    const raw = JSON.parse(readFileSync(OPENCLAW_CONFIG_PATH, "utf-8"));
    anthropicApiKey = raw?.env?.ANTHROPIC_API_KEY || "";
  } catch {
  }
  return anthropicApiKey;
}
async function callAnthropicHaiku(prompt, callback, timeoutMs) {
  const apiKey = getAnthropicApiKey();
  if (!apiKey) {
    console.log("[cc-soul][haiku] no ANTHROPIC_API_KEY, falling back to CLI");
    callback("");
    return;
  }
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const resp = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": apiKey,
        "anthropic-version": "2023-06-01"
      },
      body: JSON.stringify({
        model: HAIKU_MODEL,
        max_tokens: 2048,
        messages: [{ role: "user", content: prompt }]
      }),
      signal: controller.signal
    });
    clearTimeout(timer);
    if (!resp.ok) {
      const errText = await resp.text().catch(() => "");
      console.error(`[cc-soul][haiku] API error ${resp.status}: ${errText.slice(0, 200)}`);
      callback("");
      return;
    }
    const data = await resp.json();
    const content = data.content?.[0]?.text || "";
    console.log(`[cc-soul][haiku] ok: ${content.length} chars, ${data.usage?.input_tokens || 0}+${data.usage?.output_tokens || 0} tokens`);
    callback(content.trim());
  } catch (e) {
    clearTimeout(timer);
    if (e.name === "AbortError") {
      console.log(`[cc-soul][haiku] timeout after ${timeoutMs}ms`);
    } else {
      console.error(`[cc-soul][haiku] error: ${e.message}`);
    }
    callback("");
  }
}
const batchQueue = [];
const BATCH_MAX = 20;
const BATCH_PER_TICK = 5;
function isBatchWindow() {
  const h = (/* @__PURE__ */ new Date()).getHours();
  return h >= 2 && h < 5;
}
function queueLLMTask(prompt, callback, priority = 0, label = "batch") {
  batchQueue.push({ prompt, callback, priority, label, queuedAt: Date.now() });
  batchQueue.sort((a, b) => b.priority - a.priority);
  console.log(`[cc-soul][batch] queued: ${label} (pri=${priority}, total=${batchQueue.length})`);
  if (batchQueue.length > BATCH_MAX) {
    console.log(`[cc-soul][batch] overflow (>${BATCH_MAX}), draining top ${BATCH_PER_TICK}`);
    drainBatchQueue(BATCH_PER_TICK);
  }
}
function drainBatchQueue(limit = BATCH_PER_TICK) {
  let processed = 0;
  while (batchQueue.length > 0 && processed < limit) {
    const task = batchQueue.shift();
    console.log(`[cc-soul][batch] processing: ${task.label} (remaining=${batchQueue.length})`);
    spawnCLI(task.prompt, task.callback, 12e4, `batch:${task.label}`);
    processed++;
  }
}
function tickBatchQueue() {
  if (batchQueue.length === 0) return;
  if (!isBatchWindow()) {
    console.log(`[cc-soul][batch] ${batchQueue.length} tasks queued, waiting for 2-5 AM window`);
    return;
  }
  console.log(`[cc-soul][batch] AM window active, draining up to ${BATCH_PER_TICK}`);
  drainBatchQueue();
}
function getBatchQueueStatus() {
  return { queued: batchQueue.length, labels: batchQueue.slice(0, 5).map((t) => t.label) };
}
const EMPTY_RESULT = {
  memories: [],
  entities: [],
  satisfaction: "NEUTRAL",
  quality: { score: 5, issues: [] },
  emotion: "neutral",
  reflection: null
};
function runPostResponseAnalysis(userMsg, botResponse, callback) {
  const prompt = `\u5206\u6790\u4EE5\u4E0B\u5BF9\u8BDD\uFF0C\u4E25\u683C\u6309JSON\u8F93\u51FA\uFF08\u4E0D\u8981\u5176\u4ED6\u6587\u5B57\uFF09\uFF1A

\u7528\u6237: "${userMsg.slice(0, 500)}"
\u56DE\u590D: "${botResponse.slice(0, 500)}"

\u8BF7\u540C\u65F6\u5B8C\u6210\u4EE5\u4E0B\u5206\u6790\uFF1A
1. memories: \u63D0\u53D6\u503C\u5F97\u957F\u671F\u8BB0\u4F4F\u7684\u4FE1\u606F\u3002\u6BCF\u6761: {"content":"\u5185\u5BB9","scope":"\u7C7B\u578B","visibility":"\u53EF\u89C1\u6027"}\uFF0Cscope\u53EA\u80FD\u662F: preference/fact/event/opinion\u3002visibility\u53EA\u80FD\u662F: global(\u901A\u7528\u77E5\u8BC6/\u6280\u672F\u4E8B\u5B9E\uFF0C\u5BF9\u6240\u6709\u4EBA\u6709\u7528)/channel(\u9891\u9053\u76F8\u5173\uFF0C\u53EA\u5728\u5F53\u524D\u7FA4\u6709\u7528)/private(\u4E2A\u4EBA\u76F8\u5173\uFF0C\u53EA\u5BF9\u5F53\u524D\u7528\u6237\u6709\u7528)\u3002\u6CA1\u6709\u5C31\u7A7A\u6570\u7EC4\u3002
2. memory_ops: \u57FA\u4E8E\u5BF9\u8BDD\u5185\u5BB9\u5224\u65AD\u662F\u5426\u9700\u8981\u4FEE\u6539\u5DF2\u6709\u8BB0\u5FC6\u3002\u6BCF\u6761: {"action":"update/delete","keyword":"\u5339\u914D\u5173\u952E\u8BCD","reason":"\u539F\u56E0","new_content":"\u65B0\u5185\u5BB9(\u4EC5update\u9700\u8981)"}\u3002\u4F8B\u5982\u7528\u6237\u8BF4"\u6211\u6362\u5DE5\u4F5C\u4E86"\u2192\u5220\u9664\u65E7\u516C\u53F8\u8BB0\u5FC6+\u65B0\u589E\u65B0\u516C\u53F8\u3002\u6CA1\u6709\u5C31\u7A7A\u6570\u7EC4\u3002
3. entities: \u63D0\u53D6\u4EBA\u540D\u3001\u9879\u76EE\u540D\u3001\u516C\u53F8\u540D\u3001\u6280\u672F\u540D\u3002\u6BCF\u6761: {"name":"\u540D","type":"\u7C7B\u578B","relation":"\u5173\u7CFB"}\uFF0Ctype\u53EA\u80FD\u662F: person/project/company/tech/place\u3002\u6CA1\u6709\u5C31\u7A7A\u6570\u7EC4\u3002
4. satisfaction: \u5224\u65AD\u7528\u6237\u5BF9\u56DE\u590D\u7684\u6EE1\u610F\u5EA6: POSITIVE/NEUTRAL/NEGATIVE/TOO_VERBOSE
5. quality: \u56DE\u590D\u8D28\u91CF\u8BC4\u52061-10 + \u95EE\u9898\u5217\u8868\u3002{"score":N,"issues":["\u95EE\u9898"]}
6. emotion: \u5BF9\u8BDD\u60C5\u611F\u6807\u7B7E: neutral/warm/important/painful/funny
7. reflection: \u56DE\u590D\u6709\u4EC0\u4E48\u9057\u61BE\u6216\u53EF\u6539\u8FDB\u7684\uFF1F1\u53E5\u8BDD\uFF0C\u6CA1\u6709\u5C31null

JSON\u683C\u5F0F(\u4E25\u683C):
{"memories":[],"memory_ops":[],"entities":[],"satisfaction":"NEUTRAL","quality":{"score":5,"issues":[]},"emotion":"neutral","reflection":null}`;
  spawnCLI(
    prompt,
    (output) => {
      try {
        const result = extractJSON(output);
        if (result) {
          const rawScore = result.quality?.score;
          const clampedScore = typeof rawScore === "number" ? Math.max(1, Math.min(10, Math.round(rawScore))) : 5;
          let satisfaction = result.satisfaction || "NEUTRAL";
          const validSatisfactions = ["POSITIVE", "NEUTRAL", "NEGATIVE", "TOO_VERBOSE"];
          if (!validSatisfactions.includes(satisfaction)) satisfaction = "NEUTRAL";
          const userLower = userMsg.toLowerCase();
          const hasNegativeSignal = /不行|不对|错了|有问题|别|不要|不好|差|垃圾|废话|no|wrong|bad|stop|don't/.test(userLower);
          const hasPositiveSignal = /谢|好的|棒|赞|感谢|不错|厉害|可以|thank|great|good|nice|perfect|awesome/.test(userLower);
          if (satisfaction === "POSITIVE" && hasNegativeSignal && !hasPositiveSignal) {
            console.log(`[cc-soul][anti-hallucination] satisfaction POSITIVE\u2192NEUTRAL: user msg has negative signals`);
            satisfaction = "NEUTRAL";
          }
          if (satisfaction === "NEGATIVE" && hasPositiveSignal && !hasNegativeSignal) {
            console.log(`[cc-soul][anti-hallucination] satisfaction NEGATIVE\u2192NEUTRAL: user msg has positive signals`);
            satisfaction = "NEUTRAL";
          }
          const MAX_MEMORIES_PER_TURN = 5;
          const MAX_OPS_PER_TURN = 3;
          const memories = (result.memories || []).slice(0, MAX_MEMORIES_PER_TURN).map((m) => ({
            content: m.content,
            scope: m.scope,
            visibility: m.visibility || void 0
          })).filter((m) => m.content && m.content.length >= 3);
          const memoryOps = (result.memory_ops || []).slice(0, MAX_OPS_PER_TURN).map((op) => ({
            action: op.action,
            keyword: op.keyword || "",
            reason: op.reason || "",
            newContent: op.new_content || ""
          }));
          callback({
            memories,
            memoryOps,
            entities: (result.entities || []).slice(0, 10),
            satisfaction,
            quality: { score: clampedScore, issues: result.quality?.issues || [] },
            emotion: result.emotion || "neutral",
            reflection: result.reflection || null
          });
          return;
        }
      } catch (e) {
        console.error(`[cc-soul][ai] analysis parse error: ${e.message}`);
      }
      callback({ ...EMPTY_RESULT });
    },
    45e3
  );
}
export {
  AI_CONFIG_PATH,
  LLM_PROVIDERS,
  drainBatchQueue,
  getAIConfig,
  getActiveTaskStatus,
  getAgentBusy,
  getBatchQueueStatus,
  getFallbackApiConfig,
  getLLMStatus,
  getWorkloadCosts,
  hasLLM,
  hotReloadIfChanged,
  isCliDegraded,
  killGatewayClaude,
  loadAIConfig,
  queueLLMTask,
  runPostResponseAnalysis,
  saveLLMConfig,
  setAgentBusy,
  setFallbackApiConfig,
  setOnTaskDone,
  spawnCLI,
  tickBatchQueue,
  validateLLM
};
