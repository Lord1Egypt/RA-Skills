import { closeSync, existsSync, openSync, readFileSync, readSync, statSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { homedir } from "node:os";
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { runPluginCommandWithTimeout } from "openclaw/plugin-sdk/run-command";

const PLUGIN_DIR = dirname(fileURLToPath(import.meta.url));
const COMMON_SKILL_ROOT = "~/.openclaw/workspace/skills/cypher-tempre-self-model";
const markedRuns = new Set();

function expandHome(input) {
  if (!input || typeof input !== "string") {
    return "";
  }
  if (input === "~") {
    return homedir();
  }
  if (input.startsWith("~/")) {
    return resolve(homedir(), input.slice(2));
  }
  return resolve(input);
}

function pluginConfig(event, api) {
  const fromEvent = event?.context?.pluginConfig;
  if (fromEvent && typeof fromEvent === "object") {
    return fromEvent;
  }
  const fromApi = api?.pluginConfig;
  if (fromApi && typeof fromApi === "object") {
    return fromApi;
  }
  return {};
}

function resolveSkillRoot(config) {
  const configured = config.skillRoot || process.env.CT_SKILL_DIR;
  if (configured) {
    return expandHome(String(configured));
  }

  const nestedSkillRoot = resolve(PLUGIN_DIR, "..");
  if (existsSync(resolve(nestedSkillRoot, "enforce.py"))) {
    return nestedSkillRoot;
  }

  return expandHome(COMMON_SKILL_ROOT);
}

function resolveChainRoot(config, skillRoot) {
  const configured = config.chainRoot || process.env.CT_ENFORCE_ROOT;
  return configured ? expandHome(String(configured)) : skillRoot;
}

function numberConfig(value, fallback, min, max) {
  const n = Number(value);
  if (!Number.isFinite(n)) {
    return fallback;
  }
  return Math.min(max, Math.max(min, Math.trunc(n)));
}

function commandContext(event, api) {
  const config = pluginConfig(event, api);
  const skillRoot = resolveSkillRoot(config);
  const chainRoot = resolveChainRoot(config, skillRoot);
  const pythonBin = typeof config.pythonBin === "string" && config.pythonBin.trim()
    ? config.pythonBin.trim()
    : "python3";
  const timeoutMs = numberConfig(config.timeoutMs, 5000, 250, 30000);
  const maxFinalizeAttempts = numberConfig(config.maxFinalizeAttempts, 3, 1, 10);

  return {
    config,
    skillRoot,
    chainRoot,
    pythonBin,
    timeoutMs,
    maxFinalizeAttempts,
  };
}

async function runPython(ctx, scriptName, args = []) {
  const scriptPath = resolve(ctx.skillRoot, scriptName);
  if (!existsSync(scriptPath)) {
    return {
      ok: false,
      stdout: "",
      stderr: `missing ${scriptName} at ${scriptPath}`,
      status: 127,
    };
  }

  try {
    const result = await runPluginCommandWithTimeout({
      argv: [ctx.pythonBin, scriptPath, ...args, "--root", ctx.chainRoot],
      cwd: ctx.skillRoot,
      timeoutMs: ctx.timeoutMs,
      env: {
        ...process.env,
        CT_ENFORCE_ROOT: ctx.chainRoot,
      },
    });

    return {
      ok: result.code === 0,
      stdout: result.stdout || "",
      stderr: result.stderr || "",
      status: result.code,
    };
  } catch (error) {
    return {
      ok: false,
      stdout: "",
      stderr: error instanceof Error ? error.message : String(error),
      status: 1,
    };
  }
}

async function runEnforce(ctx, command) {
  return runPython(ctx, "enforce.py", [command]);
}

async function isDormant(ctx) {
  const result = await runPython(ctx, "dormancy.py", ["status"]);
  const firstLine = `${result.stdout}\n${result.stderr}`.trim().split(/\r?\n/, 1)[0] || "";
  return /^\s*(paused|dormant)\b/i.test(firstLine);
}

function turnKey(event, ctx) {
  return String(
    ctx?.runId ||
    event?.runId ||
    event?.context?.runId ||
    ctx?.sessionKey ||
    event?.sessionKey ||
    "",
  );
}

function reminder(ctx, dormant) {
  if (dormant) {
    return `[Cypher Tempre] DORMANT: the self-model loop is paused. Resume with: python3 ${resolve(ctx.skillRoot, "dormancy.py")} resume`;
  }

  return [
    "[Cypher Tempre] ACTIVE (non-negotiable): wear the self-model every turn.",
    "STEP 1 — route BEFORE reasoning:",
    `python3 ${resolve(ctx.skillRoot, "router.py")} route "<request>"`,
    "REPLAY -> confirm the sealed antecedent, replay.py accept, ground on it — do NOT regenerate.",
    "PARTIAL -> fetch the named rings, reason ONLY over the missing delta, seal with --used-rings.",
    "MODEL -> full loop:",
    `python3 ${resolve(ctx.skillRoot, "recall.py")} turn "<thought>" --input "<request>"`,
    "(verify -> immune-screen -> recall -> modalities/senses -> PoQ-gate -> seal; growth fires on genuine gaps).",
    "The chain answers first; the model fills gaps. Every turn seals a ring either way.",
  ].join(" ");
}

function parseBlockReason(stdout) {
  const text = String(stdout || "").trim();
  if (!text) {
    return "";
  }
  try {
    const parsed = JSON.parse(text);
    if (parsed && parsed.decision === "block") {
      return String(parsed.reason || text);
    }
  } catch {
    // Non-JSON output is still treated as an enforcement nudge.
  }
  return text;
}

function readTailText(filePath, maxBytes = 65536) {
  if (!existsSync(filePath)) {
    return "";
  }
  const fd = openSync(filePath, "r");
  try {
    const size = statSync(filePath).size;
    const length = Math.min(size, maxBytes);
    const buffer = Buffer.alloc(length);
    readSync(fd, buffer, 0, length, size - length);
    return buffer.toString("utf8");
  } finally {
    closeSync(fd);
  }
}

function currentHeadIndex(chainRoot) {
  try {
    const text = readTailText(resolve(chainRoot, "chain", "rings.jsonl"));
    const lines = text.trim().split(/\r?\n/).filter(Boolean);
    for (let i = lines.length - 1; i >= 0; i -= 1) {
      try {
        const ring = JSON.parse(lines[i]);
        if (Number.isInteger(ring.index)) {
          return ring.index;
        }
      } catch {
        // Keep scanning backward through any partial tail fragment.
      }
    }
  } catch {
    // Diagnostic only.
  }
  return -1;
}

function enforcementBaseline(chainRoot) {
  try {
    const text = readFileSync(resolve(chainRoot, "chain", ".enforce.json"), "utf8");
    const parsed = JSON.parse(text);
    return Number.isInteger(parsed.turn_head) ? parsed.turn_head : null;
  } catch {
    return null;
  }
}

function register(api) {
  api.on(
    "session_start",
    async (event, hookCtx) => {
      const ctx = commandContext(event, api);
      const result = await runEnforce(ctx, "session-start");
      if (!result.ok && result.stderr) {
        api.logger?.warn?.(`[cypher-tempre] session-start failed open: ${result.stderr}`);
      } else if (result.stdout.trim()) {
        api.logger?.info?.(result.stdout.trim());
      }
    },
    { priority: 100, timeoutMs: 30000 },
  );

  api.on(
    "before_prompt_build",
    async (event, hookCtx) => {
      const ctx = commandContext(event, api);
      const key = turnKey(event, hookCtx);
      if (!key || !markedRuns.has(key)) {
        const result = await runEnforce(ctx, "mark");
        if (result.ok && key) {
          markedRuns.add(key);
        } else if (!result.ok && result.stderr) {
          api.logger?.warn?.(`[cypher-tempre] mark failed open: ${result.stderr}`);
        }
      }

      if (ctx.config.injectReminder === false) {
        return;
      }

      return {
        appendSystemContext: reminder(ctx, await isDormant(ctx)),
      };
    },
    { priority: 100, timeoutMs: 30000 },
  );

  api.on(
    "before_agent_finalize",
    async (event, hookCtx) => {
      const ctx = commandContext(event, api);
      const result = await runEnforce(ctx, "stop-check");
      if (!result.ok && result.stderr) {
        api.logger?.warn?.(`[cypher-tempre] stop-check failed open: ${result.stderr}`);
        return;
      }

      const reason = parseBlockReason(result.stdout);
      if (!reason) {
        return;
      }

      const key = turnKey(event, hookCtx) || "unknown-run";
      return {
        action: "revise",
        reason,
        retry: {
          instruction: reason,
          idempotencyKey: `cypher-tempre-enforcement:${key}`,
          maxAttempts: ctx.maxFinalizeAttempts,
        },
      };
    },
    { priority: 100, timeoutMs: 30000 },
  );

  api.on(
    "subagent_ended",
    async (event, hookCtx) => {
      const ctx = commandContext(event, api);
      const start = enforcementBaseline(ctx.chainRoot);
      const head = currentHeadIndex(ctx.chainRoot);
      if (start !== null && head <= start) {
        api.logger?.warn?.(
          `[cypher-tempre] subagent_ended observed with no fresh sealed ring since mark (start=${start}, head=${head}).`,
        );
      }
    },
    { priority: 100, timeoutMs: 30000 },
  );

  api.on(
    "agent_end",
    async (event, hookCtx) => {
      const key = turnKey(event, hookCtx);
      if (key) {
        markedRuns.delete(key);
      }
    },
    { priority: 100, timeoutMs: 30000 },
  );
}

export default definePluginEntry({
  id: "cypher-tempre-enforcement",
  name: "Cypher Tempre Enforcement",
  description: "Routes OpenClaw turns through the Cypher Tempre Timechain enforcement spine.",
  register,
});
