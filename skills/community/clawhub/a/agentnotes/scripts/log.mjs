#!/usr/bin/env node
/**
 * AgentNotes log helper for OpenClaw
 * Usage: node log.mjs "message" [--step NAME] [--data JSON] [--error]
 */

import { getAgentNotesConfig } from "./config.mjs";

const { apiKey, agentId, logUrl } = getAgentNotesConfig();

if (!apiKey || !agentId) {
  console.error("Set AGENTNOTES_API_KEY and AGENTNOTES_AGENT_ID");
  process.exit(1);
}

const args = process.argv.slice(2);
let message = "";
let stepName = null;
let data = null;
let isError = false;

for (let i = 0; i < args.length; i++) {
  if (args[i] === "--step" && args[i + 1]) {
    stepName = args[++i];
  } else if (args[i] === "--data" && args[i + 1]) {
    data = JSON.parse(args[++i]);
  } else if (args[i] === "--error") {
    isError = true;
    message = args[++i] || "Error";
  } else if (!args[i].startsWith("--")) {
    message = args[i];
  }
}

const runId = process.env.AGENTNOTES_RUN_ID || undefined;

const res = await fetch(logUrl, {
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
        step_name: stepName,
        event_type: isError ? "error" : "log",
        message: message || (isError ? "Error" : "log"),
        data,
      },
    ],
  }),
});

if (!res.ok) {
  console.error(await res.text());
  process.exit(1);
}

const body = await res.json();
if (body.run_id) {
  console.log(body.run_id);
}
