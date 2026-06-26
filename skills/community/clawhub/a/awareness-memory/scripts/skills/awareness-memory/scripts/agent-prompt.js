#!/usr/bin/env node
// ⚠️ DO NOT EDIT — auto-generated from sdks/_shared/scripts/agent-prompt.js
// Edit the source in sdks/_shared/scripts/ then run:
//   bash scripts/sync-shared-scripts.sh
// See docs/features/f-036/shared-scripts-consolidation.md

// ---------------------------------------------------------------------------
// awareness_get_agent_prompt — Fetch activation prompt for a sub-agent role
// Usage: node agent-prompt.js role=developer_agent
// ---------------------------------------------------------------------------

const { loadConfig, resolveEndpoint, mcpCall, apiGet, parseArgs } = require("./shared");

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

  if (ep.mode === "local") {
    // Local daemon: use MCP
    const result = await mcpCall(ep.localUrl, "awareness_get_agent_prompt", {
      agent_role: role,
    });
    console.log(typeof result === "string" ? result : JSON.stringify(result, null, 2));
  } else {
    // Cloud: GET /agents then filter client-side (no /agents/prompt endpoint)
    const params = new URLSearchParams();
    if (config.agentRole) params.set("agent_role", config.agentRole);
    const agents = await apiGet(ep.baseUrl, ep.apiKey, `/memories/${ep.memoryId}/agents`, params);

    const profiles = agents.agent_profiles || agents || [];
    const match = Array.isArray(profiles)
      ? profiles.find(a => a.role === role || a.agent_role === role)
      : null;

    if (match) {
      console.log(JSON.stringify({
        agent_role: role,
        activation_prompt: match.activation_prompt || match.prompt || "",
        description: match.description || "",
      }, null, 2));
    } else {
      console.log(JSON.stringify({
        error: `No agent profile found for role: ${role}`,
        available_roles: Array.isArray(profiles) ? profiles.map(a => a.role || a.agent_role) : [],
      }, null, 2));
    }
  }
}

main().catch(e => { console.error(`[awareness] agent-prompt failed: ${e.message}`); process.exit(1); });
