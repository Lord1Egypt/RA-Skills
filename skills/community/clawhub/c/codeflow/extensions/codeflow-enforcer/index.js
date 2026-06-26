const PLUGIN_ID = "codeflow-enforcer";
const DEFAULT_QUERY_CACHE_MS = 750;
const DEFAULT_COMMAND_TIMEOUT_MS = 15000;

const BLOCKED_MUTATION_TOOLS = new Set(["write", "edit", "apply_patch"]);
const BLOCKED_SUBAGENT_TOOLS = new Set(["sessions_spawn", "subagents"]);
const ALLOWED_CODEFLOW_SUBCOMMANDS = new Set([
  "run",
  "review",
  "parallel",
  "resume",
  "guard",
  "check",
  "smoke",
]);

function nowMs() {
  return Date.now();
}

function norm(value) {
  return typeof value === "string" ? value.trim() : "";
}

function lower(value) {
  return norm(value).toLowerCase();
}

function escapeRegex(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function tailText(value, maxChars = 400) {
  const text = norm(value);
  if (!text) {
    return "";
  }
  return text.length <= maxChars ? text : text.slice(text.length - maxChars);
}

function resolvePlatformFromSessionKey(sessionKey) {
  const value = norm(sessionKey);
  if (!value) {
    return "";
  }
  for (const channel of ["telegram", "discord"]) {
    if (value.includes(`:${channel}:`)) {
      return channel;
    }
  }
  return "";
}

function formatFailure(prefix, result) {
  const stderr = tailText(result?.stderr);
  const stdout = tailText(result?.stdout);
  const detail = stderr || stdout || "Unknown error.";
  return `${prefix}\n${detail}`;
}

function normalizeCommandForMatch(command) {
  return norm(command).replace(/\s+/g, " ");
}

function extractExecCommand(params) {
  if (!params || typeof params !== "object") {
    return "";
  }
  return norm(params.command);
}

function createRuntimeCommandRunner(api, commandTimeoutMs) {
  const systemRuntime = api.runtime?.system;
  const legacyRuntime = api.runtime;
  const systemRunner =
    typeof systemRuntime?.runCommandWithTimeout === "function"
      ? systemRuntime.runCommandWithTimeout.bind(systemRuntime)
      : null;
  const legacyRunner =
    typeof legacyRuntime?.runCommandWithTimeout === "function"
      ? legacyRuntime.runCommandWithTimeout.bind(legacyRuntime)
      : null;

  let degraded = false;
  let warnedMissing = false;
  let warnedError = false;

  function warnOnce(kind, message) {
    if (kind === "missing") {
      if (warnedMissing) {
        return;
      }
      warnedMissing = true;
    } else if (kind === "error") {
      if (warnedError) {
        return;
      }
      warnedError = true;
    }
    api.logger.warn(message);
  }

  return async function runCommand(argv, env) {
    if (degraded) {
      return null;
    }

    const runner = systemRunner || legacyRunner;
    if (!runner) {
      degraded = true;
      warnOnce(
        "missing",
        `[${PLUGIN_ID}] runtime command execution is unavailable; Codeflow enforcement will fail open.`,
      );
      return null;
    }

    try {
      return await runner(argv, {
        timeoutMs: commandTimeoutMs,
        env: env ? { ...process.env, ...env } : process.env,
      });
    } catch (error) {
      degraded = true;
      warnOnce(
        "error",
        `[${PLUGIN_ID}] runtime command execution failed; Codeflow enforcement will fail open: ${String(error)}`,
      );
      return null;
    }
  };
}

function isAllowedCodeflowExec(command, codeflowScript) {
  const normalized = normalizeCommandForMatch(command);
  if (!normalized) {
    return false;
  }

  const escapedPath = escapeRegex(codeflowScript);
  const subcmd = Array.from(ALLOWED_CODEFLOW_SUBCOMMANDS).join("|");
  const direct = new RegExp(
    `^(?:(?:bash|sh)\\s+)?["']?${escapedPath}["']?\\s+(?:${subcmd})(?:\\s|$)`,
    "i",
  );
  if (direct.test(normalized)) {
    return true;
  }

  const piped = new RegExp(
    `^(?:cat\\s+<<['"][^'"]+['"]|printf\\s+[^|]+|echo\\s+[^|]+)\\s*\\|\\s*["']?${escapedPath}["']?\\s+(?:run|review|parallel|resume)(?:\\s|$)`,
    "i",
  );
  return piped.test(normalized);
}

const plugin = {
  id: PLUGIN_ID,
  name: "Codeflow Enforcer",
  description: "Thread-scoped hard enforcement for Codeflow skill workflows.",
  register(api) {
    const commandTimeoutMs =
      typeof api.pluginConfig?.commandTimeoutMs === "number" &&
      Number.isFinite(api.pluginConfig.commandTimeoutMs) &&
      api.pluginConfig.commandTimeoutMs >= 1000
        ? Math.trunc(api.pluginConfig.commandTimeoutMs)
        : DEFAULT_COMMAND_TIMEOUT_MS;
    const queryCacheMs =
      typeof api.pluginConfig?.queryCacheMs === "number" &&
      Number.isFinite(api.pluginConfig.queryCacheMs) &&
      api.pluginConfig.queryCacheMs >= 0
        ? Math.trunc(api.pluginConfig.queryCacheMs)
        : DEFAULT_QUERY_CACHE_MS;
    const blockSubagents = api.pluginConfig?.blockSubagents !== false;
    const codeflowScript = api.resolvePath("../../scripts/codeflow");
    const stateCache = new Map();
    const runRuntimeCommand = createRuntimeCommandRunner(api, commandTimeoutMs);

    async function runCodeflow(argv, env) {
      return runRuntimeCommand(["bash", codeflowScript, ...argv], env);
    }

    function invalidateState(sessionKey) {
      const key = norm(sessionKey);
      if (!key) {
        return;
      }
      stateCache.delete(key);
    }

    async function queryCurrent(sessionKey) {
      const key = norm(sessionKey);
      if (!key) {
        return null;
      }

      const cached = stateCache.get(key);
      if (cached && nowMs() - cached.ts <= queryCacheMs) {
        return cached.state;
      }

      const platform = resolvePlatformFromSessionKey(key);
      const result = await runCodeflow(["guard", "current", "-P", platform || "auto"], {
        OPENCLAW_SESSION_KEY: key,
        OPENCLAW_SESSION: key,
      });
      if (!result) {
        stateCache.set(key, { state: null, ts: nowMs() });
        return null;
      }
      if (result.code !== 0) {
        stateCache.set(key, { state: null, ts: nowMs() });
        api.logger.warn(
          `[${PLUGIN_ID}] guard current failed for ${key}: ${tailText(result.stderr || result.stdout)}`,
        );
        return null;
      }

      try {
        const state = JSON.parse(result.stdout || "{}");
        stateCache.set(key, { state, ts: nowMs() });
        return state;
      } catch (error) {
        stateCache.set(key, { state: null, ts: nowMs() });
        api.logger.warn(`[${PLUGIN_ID}] guard current JSON parse failed: ${String(error)}`);
        return null;
      }
    }

    async function deactivate(sessionKey) {
      const key = norm(sessionKey);
      if (!key) {
        return "Codeflow enforcer could not resolve this session.";
      }
      invalidateState(key);
      const platform = resolvePlatformFromSessionKey(key);
      const result = await runCodeflow(["guard", "deactivate", "-P", platform || "auto"], {
        OPENCLAW_SESSION_KEY: key,
        OPENCLAW_SESSION: key,
      });
      if (!result) {
        return "Codeflow enforcement reset skipped because runtime command execution is unavailable.";
      }
      if (result.code !== 0) {
        return formatFailure("Codeflow enforcement disable failed.", result);
      }
      return "Codeflow enforcement disabled for this thread.";
    }

    api.registerHook(
      ["command:new", "command:reset"],
      async (event) => {
        const key = norm(event.sessionKey);
        if (!key) {
          return;
        }
        const reply = await deactivate(key);
        invalidateState(key);
        api.logger.info?.(`[${PLUGIN_ID}] ${event.action}: ${reply}`);
      },
      {
        name: `${PLUGIN_ID}.session-reset`,
        description: "Deactivate Codeflow enforcement when the session is reset.",
      },
    );

    api.on(
      "before_prompt_build",
      async (_event, ctx) => {
        const sessionKey = norm(ctx.sessionKey);
        if (!sessionKey) {
          return;
        }
        const state = await queryCurrent(sessionKey);
        if (!state?.active) {
          return;
        }
        return {
          prependContext: [
            "Codeflow Enforced = ON for this thread.",
            `Coding, development, and review work must run via \`${codeflowScript} run|review|parallel|resume\`.`,
            "Direct write/edit/apply_patch/exec tool usage is blocked.",
            "If workdir is missing, ask for it. If the user wants to exit this mode, use /codeflow off.",
          ].join("\n"),
        };
      },
      { priority: 1000 },
    );

    api.on(
      "before_tool_call",
      async (event, ctx) => {
        const sessionKey = norm(ctx.sessionKey);
        if (!sessionKey) {
          return;
        }

        const state = await queryCurrent(sessionKey);
        if (!state?.active) {
          return;
        }

        const toolName = lower(event.toolName);
        if (BLOCKED_MUTATION_TOOLS.has(toolName)) {
          return {
            block: true,
            blockReason:
              "Codeflow is enforced for this thread. Direct file mutation is blocked; use Codeflow instead.",
          };
        }

        if (toolName === "exec") {
          const command = extractExecCommand(event.params);
          if (!isAllowedCodeflowExec(command, codeflowScript)) {
            return {
              block: true,
              blockReason: `Codeflow is enforced for this thread. Direct exec is blocked; use ${codeflowScript} run|review|parallel|resume|guard|check|smoke.`,
            };
          }
        }

        if (blockSubagents && BLOCKED_SUBAGENT_TOOLS.has(toolName)) {
          return {
            block: true,
            blockReason:
              "Codeflow is enforced for this thread. Subagent/session spawning is blocked; route the work through Codeflow.",
          };
        }

        return;
      },
      { priority: 1000 },
    );
  },
};

export default plugin;
