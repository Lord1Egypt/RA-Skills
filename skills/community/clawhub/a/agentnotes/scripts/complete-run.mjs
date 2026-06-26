#!/usr/bin/env node
/**
 * Complete an AgentNotes run (OpenClaw)
 * Usage: node complete-run.mjs [--result JSON] [--failed] [--run-id UUID]
 */

import { getAgentNotesConfig } from "./config.mjs";

const { apiKey, agentId, completeUrl } = getAgentNotesConfig();

if (!apiKey || !agentId) {
  console.error("Set AGENTNOTES_API_KEY and AGENTNOTES_AGENT_ID");
  process.exit(1);
}

let runId = process.env.AGENTNOTES_RUN_ID;
let result = null;
let status = "completed";
let errorMessage = null;

const args = process.argv.slice(2);
for (let i = 0; i < args.length; i++) {
  if (args[i] === "--run-id" && args[i + 1]) runId = args[++i];
  else if (args[i] === "--result" && args[i + 1]) result = JSON.parse(args[++i]);
  else if (args[i] === "--summary" && args[i + 1]) {
    result = { summary: args[++i] };
  } else if (args[i] === "--failed") status = "failed";
  else if (args[i] === "--error" && args[i + 1]) errorMessage = args[++i];
}

if (!runId) {
  console.error("Set AGENTNOTES_RUN_ID or pass --run-id");
  process.exit(1);
}

const res = await fetch(completeUrl, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${apiKey}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    agent_id: agentId,
    run_id: runId,
    result,
    status,
    error_message: errorMessage,
  }),
});

if (!res.ok) {
  console.error(await res.text());
  process.exit(1);
}

console.log("ok");
