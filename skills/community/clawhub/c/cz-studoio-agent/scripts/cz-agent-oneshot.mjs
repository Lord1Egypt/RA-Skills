#!/usr/bin/env node

import { randomUUID } from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import process from "node:process";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";

const SKILL_KEY = "studio-agent";
const DEFAULT_CONFIG_PATH = "~/.openclaw/clawdbot.json";
const SETUP_CONFIG_FILE = "studio-agent.config.json";
const SETUP_COMMANDS = [
  `cp skills/studio-agent/studio-agent.config.example.json ${SETUP_CONFIG_FILE}`,
  `node skills/studio-agent/scripts/configure-skill.mjs validate --input ${SETUP_CONFIG_FILE}`,
  `node skills/studio-agent/scripts/configure-skill.mjs apply --input ${SETUP_CONFIG_FILE} --replace --restart`,
];

function usage() {
  return [
    "Studio Agent one-shot runner",
    "",
    "Usage:",
    "  node skills/studio-agent/scripts/cz-agent-oneshot.mjs --input <text> [options]",
    "",
    "Options:",
    "  --input <text>                    User input to send (required)",
    "  --config <path>                  OpenClaw config path (default ~/.openclaw/clawdbot.json)",
    "  --request-id <id>                Override request id (default req-<uuid>)",
    "  --request-timeout-seconds <n>    Proxy request timeout (default 120)",
    "  --startup-timeout-seconds <n>    Proxy startup connect timeout (default 12)",
    "  --hard-timeout-seconds <n>       Total process timeout (default request+startup+8)",
    "  --raw-events                     Include parsed proxy events in output JSON",
    "  -h, --help                       Show this help",
  ].join("\n");
}

function isRecord(value) {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

function asTrimmedString(value) {
  if (value === undefined || value === null) {
    return undefined;
  }
  const text = String(value).trim();
  return text.length > 0 ? text : undefined;
}

function expandHome(inputPath) {
  const raw = asTrimmedString(inputPath);
  if (!raw) {
    return raw;
  }
  if (raw.startsWith("~/")) {
    return path.join(os.homedir(), raw.slice(2));
  }
  return raw;
}

function parsePositiveInt(value, fallback) {
  const text = asTrimmedString(value);
  if (!text) {
    return fallback;
  }
  const parsed = Number.parseInt(text, 10);
  if (!Number.isFinite(parsed) || parsed <= 0) {
    return fallback;
  }
  return parsed;
}

function parseArgs(argv) {
  const args = [...argv];
  const opts = {
    input: undefined,
    configPath: DEFAULT_CONFIG_PATH,
    requestId: undefined,
    requestTimeoutSeconds: 120,
    startupTimeoutSeconds: 12,
    hardTimeoutSeconds: undefined,
    rawEvents: false,
    help: false,
  };

  while (args.length > 0) {
    const arg = args.shift();
    if (!arg) {
      continue;
    }
    if (arg === "-h" || arg === "--help") {
      opts.help = true;
      return opts;
    }
    if (arg === "--raw-events") {
      opts.rawEvents = true;
      continue;
    }
    if (arg === "--input") {
      opts.input = args.shift();
      continue;
    }
    if (arg === "--config") {
      opts.configPath = args.shift();
      continue;
    }
    if (arg === "--request-id") {
      opts.requestId = args.shift();
      continue;
    }
    if (arg === "--request-timeout-seconds") {
      opts.requestTimeoutSeconds = parsePositiveInt(args.shift(), opts.requestTimeoutSeconds);
      continue;
    }
    if (arg === "--startup-timeout-seconds") {
      opts.startupTimeoutSeconds = parsePositiveInt(args.shift(), opts.startupTimeoutSeconds);
      continue;
    }
    if (arg === "--hard-timeout-seconds") {
      opts.hardTimeoutSeconds = parsePositiveInt(args.shift(), opts.hardTimeoutSeconds);
      continue;
    }
    throw new Error(`Unknown argument: ${arg}`);
  }

  return opts;
}

function loadSkillEnv(configPath) {
  const fullPath = path.resolve(expandHome(configPath));
  const raw = fs.readFileSync(fullPath, "utf8");
  const parsed = JSON.parse(raw);
  const env = parsed?.skills?.entries?.[SKILL_KEY]?.env;
  if (!isRecord(env)) {
    throw new Error(`Missing skills.entries.${SKILL_KEY}.env in ${fullPath}`);
  }
  return { configPath: fullPath, env };
}

function collectEnv(skillEnv, opts) {
  const env = { ...process.env };
  for (const [key, value] of Object.entries(skillEnv)) {
    if (!key.startsWith("CZ_")) {
      continue;
    }
    const text = asTrimmedString(value);
    if (text !== undefined) {
      env[key] = text;
    }
  }

  env.CZ_REQUEST_TIMEOUT_SECONDS = String(opts.requestTimeoutSeconds);
  env.CZ_STARTUP_CONNECT_TIMEOUT_SECONDS = String(opts.startupTimeoutSeconds);
  if (!asTrimmedString(env.CZ_INTERRUPT_DECISION_MODE)) {
    env.CZ_INTERRUPT_DECISION_MODE = "auto_approve";
  }
  if (!asTrimmedString(env.CZ_EMIT_ASSISTANT_DELTAS)) {
    env.CZ_EMIT_ASSISTANT_DELTAS = "false";
  }

  return env;
}

function writeJsonAndExit(payload, code) {
  process.stdout.write(`${JSON.stringify(payload)}\n`);
  process.exit(code);
}

function createProtocolError(message, extra = {}) {
  return {
    ok: false,
    error: {
      code: "PROTOCOL_ERROR",
      message,
    },
    ...extra,
  };
}

function createSetupHint(configPath) {
  return {
    setup: {
      required: true,
      config_path: configPath ?? null,
      commands: [...SETUP_COMMANDS],
    },
  };
}

async function run() {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.help) {
    process.stdout.write(`${usage()}\n`);
    return;
  }

  const input = asTrimmedString(opts.input);
  if (!input) {
    writeJsonAndExit(createProtocolError("missing --input"), 1);
    return;
  }

  const requestId = asTrimmedString(opts.requestId) ?? `req-${randomUUID()}`;

  let loaded;
  try {
    loaded = loadSkillEnv(opts.configPath);
  } catch (error) {
    writeJsonAndExit(
      createProtocolError("studio-agent skill env is missing in OpenClaw config", {
        detail: error instanceof Error ? error.message : String(error),
        ...createSetupHint(expandHome(opts.configPath)),
      }),
      1,
    );
    return;
  }

  const env = collectEnv(loaded.env, opts);
  const wsUrl = asTrimmedString(env.CZ_AGENT_WS_URL);
  if (!wsUrl) {
    writeJsonAndExit(
      createProtocolError("studio-agent skill env is incomplete: missing CZ_AGENT_WS_URL", {
        config_path: loaded.configPath,
        ...createSetupHint(loaded.configPath),
      }),
      1,
    );
    return;
  }

  const proxyPath = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "cz-agent-proxy.mjs");
  const hardTimeoutSeconds =
    opts.hardTimeoutSeconds ?? opts.requestTimeoutSeconds + opts.startupTimeoutSeconds + 8;
  const hardTimeoutMs = hardTimeoutSeconds * 1000;

  const child = spawn(process.execPath, [proxyPath], {
    cwd: process.cwd(),
    env,
    stdio: ["pipe", "pipe", "pipe"],
  });

  const outbound = {
    version: "v1",
    op: "user_input",
    request_id: requestId,
    user_input: input,
    metadata: {
      source: "openclaw",
      configs: [{ type: "text", value: input }],
    },
  };

  const events = [];
  const rawStdoutLines = [];
  const stderrChunks = [];

  let stdoutBuffer = "";
  let finalized = false;
  let timedOut = false;
  let parseError = false;
  let finalEvent = null;
  let errorEvent = null;

  const finalize = (exitCode, signal) => {
    if (finalized) {
      return;
    }
    finalized = true;

    const base = {
      request_id: requestId,
      config_path: loaded.configPath,
      diagnostics: {
        exit_code: exitCode,
        signal: signal ?? null,
        stderr_tail: stderrChunks.join("").slice(-2000),
      },
    };

    if (finalEvent) {
      writeJsonAndExit(
        {
          ok: true,
          content: finalEvent.content ?? "",
          conversation_id: finalEvent.conversation_id ?? null,
          event: {
            event: finalEvent.event,
            op_type: finalEvent.op_type,
            complete: finalEvent.complete,
          },
          ...(opts.rawEvents ? { events } : {}),
          ...base,
        },
        0,
      );
      return;
    }

    if (errorEvent) {
      writeJsonAndExit(
        {
          ok: false,
          error: errorEvent.error ?? {
            code: "REMOTE_ERROR",
            message: "proxy returned error event without details",
          },
          conversation_id: errorEvent.conversation_id ?? null,
          ...(opts.rawEvents ? { events } : {}),
          ...base,
        },
        1,
      );
      return;
    }

    if (timedOut) {
      writeJsonAndExit(
        {
          ok: false,
          error: {
            code: "TIMEOUT",
            message: `one-shot hard timeout after ${hardTimeoutSeconds}s`,
          },
          ...(opts.rawEvents ? { events } : {}),
          ...base,
        },
        1,
      );
      return;
    }

    if (parseError) {
      writeJsonAndExit(
        {
          ok: false,
          error: {
            code: "PROTOCOL_ERROR",
            message: "proxy stdout included non-JSON lines before completion",
          },
          raw_stdout_tail: rawStdoutLines.join("\n").slice(-2000),
          ...(opts.rawEvents ? { events } : {}),
          ...base,
        },
        1,
      );
      return;
    }

    writeJsonAndExit(
      {
        ok: false,
        error: {
          code: "REMOTE_ERROR",
          message: "proxy exited without assistant_final/error event",
        },
        raw_stdout_tail: rawStdoutLines.join("\n").slice(-2000),
        ...(opts.rawEvents ? { events } : {}),
        ...base,
      },
      1,
    );
  };

  const hardTimer = setTimeout(() => {
    timedOut = true;
    try {
      child.kill("SIGTERM");
    } catch {
      // ignore
    }
  }, hardTimeoutMs);

  child.stdout.on("data", (chunk) => {
    stdoutBuffer += chunk.toString("utf8");
    while (true) {
      const index = stdoutBuffer.indexOf("\n");
      if (index < 0) {
        break;
      }
      const line = stdoutBuffer.slice(0, index).trim();
      stdoutBuffer = stdoutBuffer.slice(index + 1);
      if (!line) {
        continue;
      }
      rawStdoutLines.push(line);

      let parsed;
      try {
        parsed = JSON.parse(line);
      } catch {
        parseError = true;
        continue;
      }

      events.push(parsed);
      const eventRequestId = asTrimmedString(parsed.request_id);
      const eventName = asTrimmedString(parsed.event);
      if (eventName === "error") {
        if (eventRequestId === STARTUP_ID || eventRequestId === requestId) {
          errorEvent = parsed;
        }
        continue;
      }
      if (eventName === "assistant_final" && eventRequestId === requestId && parsed.complete === true) {
        finalEvent = parsed;
      }
    }
  });

  child.stderr.on("data", (chunk) => {
    stderrChunks.push(chunk.toString("utf8"));
  });

  child.on("close", (code, signal) => {
    clearTimeout(hardTimer);
    finalize(code, signal);
  });

  child.stdin.write(`${JSON.stringify(outbound)}\n`);
  child.stdin.end();
}

const STARTUP_ID = "startup";

run().catch((error) => {
  writeJsonAndExit(
    createProtocolError(`unexpected runner error: ${error instanceof Error ? error.message : String(error)}`),
    1,
  );
});
