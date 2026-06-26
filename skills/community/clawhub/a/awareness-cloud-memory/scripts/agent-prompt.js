#!/usr/bin/env node
// ---------------------------------------------------------------------------
// awareness_get_agent_prompt — Fetch activation prompt for a sub-agent role
// Usage: node agent-prompt.js role=developer_agent
// ---------------------------------------------------------------------------

const { loadConfig, resolveEndpoint, apiGet, parseArgs } = require("./shared");

async function main() {
  const args = parseArgs();
  const role = args.role || args.agent_role || args.query;
  if (!role) {
    console.log(JSON.stringify({ error: "Usage: node agent-prompt.js role=<agent_role>" }));
    return;
  }

  const config = loadConfig();
  const ep = await resolveEndpoint(config);
  if (!ep) { console.log(JSON.stringify({ error: "Not configured." })); return; }

  const params = new URLSearchParams({ agent_role: role });
  const result = await apiGet(ep.baseUrl, ep.apiKey, `/memories/${ep.memoryId}/agents/prompt`, params);
  console.log(JSON.stringify(result, null, 2));
}

main().catch(e => { console.error(`[awareness] agent-prompt failed: ${e.message}`); process.exit(1); });
