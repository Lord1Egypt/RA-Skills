#!/usr/bin/env node
/** Test AgentNotes connection from OpenClaw env vars */

import { getAgentNotesConfig } from "./config.mjs";

const { apiKey, agentId, baseUrl, logUrl } = getAgentNotesConfig();

if (!apiKey || !agentId) {
  console.error("Missing AGENTNOTES_API_KEY or AGENTNOTES_AGENT_ID");
  process.exit(1);
}

console.log("AgentNotes verify");
console.log("  base:", baseUrl);
console.log("  agent:", agentId);
console.log("  key:", apiKey.slice(0, 12) + "…");

const health = await fetch(`${baseUrl}/api/v1/health`);
if (!health.ok) {
  console.error("Health check failed:", await health.text());
  process.exit(1);
}
console.log("  health: ok");

const logRes = await fetch(logUrl, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${apiKey}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    agent_id: agentId,
    logs: [
      {
        message: "OpenClaw connection test",
        event_type: "log",
        step_name: "verify",
        data: { source: "openclaw" },
      },
    ],
  }),
});

if (!logRes.ok) {
  console.error("Log test failed:", await logRes.text());
  process.exit(1);
}

const { run_id } = await logRes.json();
console.log("  log: ok, run_id:", run_id);
console.log("\nConnected. SparkNotes will roll up hourly/daily in the dashboard.");
