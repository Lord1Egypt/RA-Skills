#!/usr/bin/env node
/** Start a run; prints run_id to stdout (pipe to AGENTNOTES_RUN_ID) */

import { getAgentNotesConfig } from "./config.mjs";

const { apiKey, agentId, logUrl } = getAgentNotesConfig();

if (!apiKey || !agentId) {
  console.error("Set AGENTNOTES_API_KEY and AGENTNOTES_AGENT_ID");
  process.exit(1);
}

const res = await fetch(logUrl, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${apiKey}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    agent_id: agentId,
    logs: [{ event_type: "log", message: "run_started", data: { source: "openclaw" } }],
  }),
});

if (!res.ok) {
  console.error(await res.text());
  process.exit(1);
}

const body = await res.json();
console.log(body.run_id);
