#!/usr/bin/env node
/**
 * One-shot OpenClaw task log: start → optional log → complete with summary.
 *
 * Usage:
 *   node task.mjs --summary "Handled 3 Telegram messages"
 *   node task.mjs --summary "Cron OK" --message "Checked inbox" --step heartbeat
 *   node task.mjs --summary "Failed" --failed --error "API timeout"
 */

import { getAgentNotesConfig } from "./config.mjs";

const { apiKey, agentId, logUrl, completeUrl } = getAgentNotesConfig();

if (!apiKey || !agentId) {
  console.error("Set AGENTNOTES_API_KEY and AGENTNOTES_AGENT_ID");
  process.exit(1);
}

let summary = "";
let message = null;
let step = null;
let data = null;
let failed = false;
let errorMessage = null;

const args = process.argv.slice(2);
for (let i = 0; i < args.length; i++) {
  if (args[i] === "--summary" && args[i + 1]) summary = args[++i];
  else if (args[i] === "--message" && args[i + 1]) message = args[++i];
  else if (args[i] === "--step" && args[i + 1]) step = args[++i];
  else if (args[i] === "--data" && args[i + 1]) data = JSON.parse(args[++i]);
  else if (args[i] === "--failed") failed = true;
  else if (args[i] === "--error" && args[i + 1]) errorMessage = args[++i];
}

if (!summary) {
  console.error("Required: --summary \"What the agent did\"");
  process.exit(1);
}

const startRes = await fetch(logUrl, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${apiKey}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    agent_id: agentId,
    logs: [
      {
        event_type: "log",
        message: "openclaw_task_start",
        data: { source: "openclaw" },
      },
    ],
  }),
});

if (!startRes.ok) {
  console.error(await startRes.text());
  process.exit(1);
}

let { run_id: runId } = await startRes.json();

if (message) {
  const logRes = await fetch(logUrl, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      agent_id: agentId,
      run_id: runId,
      logs: [
        {
          step_name: step,
          event_type: failed ? "error" : "log",
          message,
          data,
        },
      ],
    }),
  });
  if (!logRes.ok) {
    console.error(await logRes.text());
    process.exit(1);
  }
  const logBody = await logRes.json();
  if (logBody.run_id) runId = logBody.run_id;
}

const completeRes = await fetch(completeUrl, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${apiKey}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    agent_id: agentId,
    run_id: runId,
    result: { summary },
    status: failed ? "failed" : "completed",
    error_message: errorMessage,
  }),
});

if (!completeRes.ok) {
  console.error(await completeRes.text());
  process.exit(1);
}

console.log("ok");
