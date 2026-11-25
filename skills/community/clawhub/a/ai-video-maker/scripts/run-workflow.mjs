#!/usr/bin/env node
import { createAIVideoClient } from "./aivideo-client.mjs";
import { TOP_UP_URL, agentPlatformArgument } from "./contract.mjs";
import { firstVideoPayload, validateFirstVideoFlow } from "./first-video.mjs";
import { prepareJobState, readJobState, saveTaskId } from "./job-state.mjs";

const TERMINAL_STATUSES = new Set(["COMPLETED", "FAILED", "CANCEL"]);

// Show only an official link, whatever a response claims.
function topUpUrl(result) {
  const candidate = result?.data?.topUpUrl;
  return typeof candidate === "string" && candidate.startsWith("https://aivideomaker.ai/")
    ? candidate
    : TOP_UP_URL;
}

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
  return Number.isFinite(n) && n > 0 ? n : fallback;
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
      `Nothing was charged and no task was created by this attempt. Tell the user the balance cannot cover this video and show this link to add API credits: ${topUpUrl(result)}`,
      "Credit packs are one-time purchases; no subscription is required. After the user adds credits, quote again and continue with the same request.",
      "Alternatively, offer a shorter duration or a lower-credit configuration and quote that instead.",
    ];
  }
  if (code === "RATE_LIMITED") {
    return [
      "Lower polling frequency and honor Retry-After first.",
      "Keep query requests within 60 req/min/IP.",
    ];
  }
  if (code === "BUDGET_EXCEEDED") {
    return [
      "Request a larger explicit budget from the user or choose a cheaper configuration.",
      "Do not remove the max-credit guard without user authorization.",
    ];
  }
  if (status === "FAILED") {
    return [
      "Check whether prompt/image inputs are valid and accessible.",
      "Confirm terminal failure before proposing a new, separately quoted generation.",
    ];
  }
  return [
    "Check request parameters and network state. Resume a known task; reuse the same key for an ambiguous submission.",
  ];
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

function finish(result, { unfinished = false } = {}) {
  print(result);
  if (!result.ok) {
    process.exitCode = unfinished ? 2 : 1;
  }
}

async function runAction(client, args) {
  const action = args.action;
  const taskId = args.taskId;

  if (action === "wait") {
    const state = args.stateFile ? await readJobState(args.stateFile) : null;
    if (state && taskId && state.taskId !== taskId)
      throw new Error("Task ID does not match the recovery state.");
    const existingTaskId = taskId || state?.taskId;
    if (!existingTaskId)
      throw new Error(
        "No task ID saved. Replay the identical request with its state file to recover the submission.",
      );
    await waitForTask(client, args, existingTaskId, state?.idempotencyKey);
    return;
  }

  if (action === "doctor") {
    const result = await client.doctor();
    finish(result);
    return;
  }

  if (action === "quote") {
    if (!args.model) throw new Error("--model is required for --action quote");
    if (!args.payload) throw new Error("--payload is required for --action quote");
    const payload = parseJsonText(args.payload, "--payload");
    const result = await client.quoteGeneration({ model: args.model, payload });
    if (result.ok && result.data?.affordable === false) {
      // The user can act on a shortfall only if they are handed the way to fix it.
      finish({
        ...result,
        topUpUrl: topUpUrl(result),
        nextStep:
          "The balance cannot cover a new request at this price. If this exact request may already have been submitted (a saved task ID, a state file, or the same first-video flow), resume or replay it unchanged first: its own charge can be what lowered the balance, and a replay never charges twice. Otherwise show the quote, the balance and the topUpUrl link for adding API credits (one-time packs, no subscription), or offer a cheaper configuration, and submit nothing new until a quote is affordable.",
      });
      return;
    }
    finish(
      args.firstVideoFlow && result.ok
        ? {
            ...result,
            nextStep:
              "Show this quote and balance to the user. Ask for approval before generation; setup alone is not spending approval.",
          }
        : result,
    );
    return;
  }

  if (action === "getStatus") {
    if (!taskId) throw new Error("--taskId is required for --action getStatus");
    const result = await client.getStatus(taskId);
    finish(result);
    return;
  }

  if (action === "getTask") {
    if (!taskId) throw new Error("--taskId is required for --action getTask");
    const result = await client.getTask(taskId);
    finish(result);
    return;
  }

  if (action === "cancelTask") {
    if (!taskId) throw new Error("--taskId is required for --action cancelTask");
    const result = await client.cancelTask(taskId);
    finish(result);
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
  if (args.maxCredits === undefined) {
    throw new Error("--maxCredits is required for billable generation");
  }
  const maxCredits = Number(args.maxCredits);
  if (!Number.isInteger(maxCredits) || maxCredits < 0) {
    throw new Error("--maxCredits must be a non-negative integer");
  }
  const quoteResult = await client.quoteGeneration({ model, payload });
  if (!quoteResult.ok) {
    finish(quoteResult);
    return;
  }
  if (Number(quoteResult.data?.credits) > maxCredits) {
    finish({
      ok: false,
      status: "FAILED",
      taskId: null,
      data: quoteResult.data,
      errorCode: "BUDGET_EXCEEDED",
      errorMessage: `Quoted cost (${quoteResult.data.credits} credits) exceeds --maxCredits ${maxCredits}`,
      suggestions: failureSuggestions({ errorCode: "BUDGET_EXCEEDED" }),
    });
    return;
  }
  // A quote sees the current balance, which may already exclude this task's debit.
  // The server resolves the stable key before enforcing balance on a new task.
  const state = args.stateFile
    ? await prepareJobState(args.stateFile, {
        model,
        payload,
        maxCredits,
        idempotencyKey: args.idempotencyKey,
      })
    : null;
  if (state?.taskId) {
    await waitForTask(client, args, state.taskId, state.idempotencyKey);
    return;
  }
  const createResult = await client.createGeneration({
    model,
    payload,
    maxCredits,
    idempotencyKey: state?.idempotencyKey || args.idempotencyKey,
  });
  if (!createResult.ok) {
    finish({
      ...createResult,
      ...(createResult.errorCode === "INSUFFICIENT_CREDITS"
        ? { topUpUrl: topUpUrl(createResult) }
        : {}),
      suggestions: failureSuggestions(createResult),
    });
    return;
  }

  const taskId = createResult.taskId;
  const idempotencyKey = createResult.idempotencyKey;
  if (args.stateFile) {
    try {
      await saveTaskId(args.stateFile, state, taskId);
    } catch {
      finish({
        ok: false,
        status: createResult.status,
        taskId,
        idempotencyKey,
        errorCode: "STATE_SAVE_FAILED",
        errorMessage:
          "Task accepted but recovery state update failed. Preserve the task ID and resume waiting; do not create a replacement.",
      });
      return;
    }
  }
  const autoPoll = String(args.autoPoll ?? "true") !== "false";
  if (!autoPoll) {
    finish(createResult);
    return;
  }

  await waitForTask(client, args, taskId, idempotencyKey, quoteResult.data);
}

async function waitForTask(client, args, taskId, idempotencyKey, quote) {
  const maxWaitMs = asNumber(args.maxWaitMs, 10 * 60 * 1000);
  const pollMinMs = asNumber(args.pollMinMs, 2000);
  const pollMaxMs = asNumber(args.pollMaxMs, 10000);

  const startedAt = Date.now();
  let currentPollMs = pollMinMs;
  let lastStatusResult = null;

  while (Date.now() - startedAt < maxWaitMs) {
    const statusResult = await client.getStatus(taskId);
    lastStatusResult = statusResult;

    const terminalResponse =
      statusResult.httpStatus >= 200 &&
      statusResult.httpStatus < 300 &&
      TERMINAL_STATUSES.has(statusResult.status);
    if (!statusResult.ok && !terminalResponse) {
      finish({
        ...statusResult,
        taskId,
        idempotencyKey,
        suggestions: [
          `Resume with --action wait --taskId ${taskId}. Do not create a replacement task.`,
        ],
      });
      return;
    }

    if (TERMINAL_STATUSES.has(statusResult.status)) {
      if (statusResult.status === "COMPLETED") {
        const detailResult = await client.getTask(taskId);
        if (!detailResult.ok) {
          finish({
            ...detailResult,
            ok: false,
            status: "COMPLETED",
            taskId,
            idempotencyKey,
            errorCode: "RETRIEVAL_FAILED",
            errorMessage:
              detailResult.errorMessage || "Generation completed but output retrieval failed",
            suggestions: [
              `Resume retrieval with --action getTask --taskId ${taskId}`,
              "Do not submit a replacement generation unless retrieval confirms the task failed.",
            ],
          });
          return;
        }
        finish({
          ...detailResult,
          idempotencyKey,
          ...(quote ? { quote } : {}),
        });
        return;
      }
      finish({
        ...statusResult,
        ok: false,
        taskId,
        idempotencyKey,
        suggestions: [
          statusResult.status === "FAILED" ? "The task failed." : "The task was cancelled.",
          "Any new generation requires a new quote and sufficient authorized budget.",
        ],
      });
      return;
    }

    await sleep(currentPollMs);
    currentPollMs = nextPollMs(currentPollMs, pollMaxMs);
  }

  finish(
    {
      ok: false,
      status: lastStatusResult?.status || "PROGRESS",
      taskId,
      idempotencyKey,
      errorCode: "POLL_TIMEOUT",
      errorMessage: `Polling exceeded max wait time (${maxWaitMs}ms)`,
      suggestions: [
        `Resume with --action wait --taskId ${taskId}; increase --maxWaitMs if needed. Do not submit again.`,
      ],
    },
    { unfinished: true },
  );
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.firstVideoFlow) {
    validateFirstVideoFlow(args.firstVideoFlow);
    if (args.model && args.model !== "minimax")
      throw new Error(
        "The first-video guide uses minimax. Use the normal workflow for other models.",
      );
    if (args.action && args.action !== "quote")
      throw new Error(
        "Use --action quote to prepare a first video. Resume tasks using their task ID without --firstVideoFlow.",
      );
    if (!args.action && args.approved !== "true")
      throw new Error(
        "Quote first, then obtain spending approval. Generation requires --approved true and --maxCredits.",
      );
    if (args.idempotencyKey && args.idempotencyKey !== `first-video:${args.firstVideoFlow}`)
      throw new Error("Reuse the first-video flow's idempotency key.");
    args.idempotencyKey = `first-video:${args.firstVideoFlow}`;
    args.model = "minimax";
  }
  const client = createAIVideoClient({
    debug: String(args.debug ?? "false") !== "false",
    // Without the argument, the client falls back to AIVIDEO_AGENT_PLATFORM.
    ...(args.platform === undefined ? {} : { agentPlatform: agentPlatformArgument(args.platform) }),
  });
  if (args.firstVideoFlow) {
    if (!["product", "social", "custom"].includes(args.scenario))
      throw new Error("Choose --scenario product, social, or custom.");
    args.payload = JSON.stringify(
      firstVideoPayload(args.scenario, parseJsonText(args.payload, "--payload")),
    );
  }

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
