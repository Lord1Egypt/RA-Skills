#!/usr/bin/env node
import { createAIVideoClient } from "./aivideo-client.mjs";

const TERMINAL_STATUSES = new Set(["COMPLETED", "FAILED", "CANCEL"]);

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) continue;
    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) {
      args[key] = true;
    } else {
      args[key] = next;
      i += 1;
    }
  }
  return args;
}

function asNumber(value, fallback) {
  const n = Number(value);
  return Number.isFinite(n) ? n : fallback;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function nextPollMs(currentMs, maxMs) {
  return Math.min(maxMs, Math.floor(currentMs * 1.5));
}

function failureSuggestions(result) {
  const code = result?.errorCode;
  const status = result?.status;
  if (code === "INSUFFICIENT_CREDITS") {
    return [
      "Reduce duration or switch to a lower-cost model (for example t2v/i2v v1).",
      "Check account credits and retry after top-up.",
    ];
  }
  if (code === "RATE_LIMITED") {
    return [
      "Lower polling frequency and honor Retry-After first.",
      "Keep query requests within 60 req/min/IP.",
    ];
  }
  if (status === "FAILED") {
    return [
      "Check whether prompt/image inputs are valid and accessible.",
      "Retry with shorter duration and lower complexity.",
    ];
  }
  return ["Check request parameters and network state, then retry."];
}

function parseJsonText(text, sourceLabel) {
  try {
    return JSON.parse(text);
  } catch (error) {
    throw new Error(`${sourceLabel} must be valid JSON`);
  }
}

function print(result) {
  // eslint-disable-next-line no-console
  console.log(JSON.stringify(result, null, 2));
}

async function runAction(client, args) {
  const action = args.action;
  const taskId = args.taskId;

  if (action === "getStatus") {
    if (!taskId) throw new Error("--taskId is required for --action getStatus");
    const result = await client.getStatus(taskId);
    print(result);
    return;
  }

  if (action === "getTask") {
    if (!taskId) throw new Error("--taskId is required for --action getTask");
    const result = await client.getTask(taskId);
    print(result);
    return;
  }

  if (action === "cancelTask") {
    if (!taskId) throw new Error("--taskId is required for --action cancelTask");
    const result = await client.cancelTask(taskId);
    print(result);
    return;
  }

  throw new Error(`Unsupported action: ${action}`);
}

async function runCreateAndPoll(client, args) {
  const model = args.model;
  const payloadText = args.payload;

  if (!model) throw new Error("--model is required");
  if (!payloadText) {
    throw new Error("--payload is required");
  }

  // Production mode: only accept runtime payload to avoid stale template files.
  const payload = parseJsonText(payloadText, "--payload");
  const createResult = await client.createGeneration({ model, payload });
  if (!createResult.ok) {
    print({
      ...createResult,
      suggestions: failureSuggestions(createResult),
    });
    return;
  }

  const taskId = createResult.taskId;
  const autoPoll = String(args.autoPoll ?? "true") !== "false";
  if (!autoPoll) {
    print(createResult);
    return;
  }

  const maxWaitMs = asNumber(args.maxWaitMs, 10 * 60 * 1000);
  const pollMinMs = asNumber(args.pollMinMs, 2000);
  const pollMaxMs = asNumber(args.pollMaxMs, 10000);

  const startedAt = Date.now();
  let currentPollMs = pollMinMs;
  let lastStatusResult = null;

  while (Date.now() - startedAt < maxWaitMs) {
    const statusResult = await client.getStatus(taskId);
    lastStatusResult = statusResult;

    if (!statusResult.ok) {
      print({
        ...statusResult,
        taskId,
        suggestions: failureSuggestions(statusResult),
      });
      return;
    }

    if (TERMINAL_STATUSES.has(statusResult.status)) {
      if (statusResult.status === "COMPLETED") {
        const detailResult = await client.getTask(taskId);
        print(detailResult.ok ? detailResult : statusResult);
        return;
      }
      print({
        ...statusResult,
        taskId,
        suggestions: failureSuggestions(statusResult),
      });
      return;
    }

    await sleep(currentPollMs);
    currentPollMs = nextPollMs(currentPollMs, pollMaxMs);
  }

  print({
    ok: false,
    status: lastStatusResult?.status || "PROGRESS",
    taskId,
    errorCode: "POLL_TIMEOUT",
    errorMessage: `Polling exceeded max wait time (${maxWaitMs}ms)`,
    suggestions: ["Increase --maxWaitMs", "Use async mode: --autoPoll false"],
  });
}

async function main() {
  const args = parseArgs(process.argv);
  const client = createAIVideoClient({
    debug: String(args.debug ?? "false") !== "false",
  });

  if (args.action) {
    await runAction(client, args);
    return;
  }

  await runCreateAndPoll(client, args);
}

main().catch((error) => {
  print({
    ok: false,
    status: "FAILED",
    errorCode: "UNCAUGHT_ERROR",
    errorMessage: error?.message || "Unhandled workflow error",
  });
  process.exitCode = 1;
});
