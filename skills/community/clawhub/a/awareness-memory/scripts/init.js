#!/usr/bin/env node
// ⚠️ DO NOT EDIT — auto-generated from sdks/_shared/scripts/init.js
// Edit the source in sdks/_shared/scripts/ then run:
//   bash scripts/sync-shared-scripts.sh
// See docs/features/f-036/shared-scripts-consolidation.md

// ---------------------------------------------------------------------------
// awareness_init — Initialize session and load cross-session context
// Usage: node init.js [days=7] [max_cards=20] [max_tasks=20]
// ---------------------------------------------------------------------------

const { loadConfig, resolveEndpoint, getSessionId, mcpCall, apiGet, parseArgs } = require("./shared");

async function main() {
  const args = parseArgs();
  const config = loadConfig();
  const ep = await resolveEndpoint(config);
  if (!ep) { console.log(JSON.stringify({ error: "Not configured. Set AWARENESS_API_KEY and AWARENESS_MEMORY_ID." })); return; }

  const sessionId = getSessionId();
  let ctx;

  if (ep.mode === "local") {
    // Local daemon: use MCP JSON-RPC
    ctx = await mcpCall(ep.localUrl, "awareness_init", {
      source: "awareness-skill",
      ...(args.query ? { query: args.query } : {}),
    });
  } else {
    // Cloud: use REST API
    const params = new URLSearchParams();
    params.set("days", String(args.days || 7));
    params.set("max_cards", String(args.max_cards || 20));
    params.set("max_tasks", String(args.max_tasks || 20));
    if (args.query) params.set("query", String(args.query));
    if (config.agentRole) params.set("agent_role", config.agentRole);
    ctx = await apiGet(ep.baseUrl, ep.apiKey, `/memories/${ep.memoryId}/context`, params);
  }

  console.log(JSON.stringify({
    session_id: ctx.session_id || sessionId,
    memory_id: ep.memoryId,
    mode: ep.mode,
    user_preferences: ctx.user_preferences || [],
    last_sessions: ctx.last_sessions || ctx.recent_sessions || [],
    recent_days: ctx.recent_days || [],
    open_tasks: ctx.open_tasks || [],
    knowledge_cards: ctx.knowledge_cards || [],
    active_skills: ctx.active_skills || [],
    attention_summary: ctx.attention_summary || null,
    stats: ctx.stats || null,
  }, null, 2));
}

main().catch(e => { console.error(`[awareness] init failed: ${e.message}`); process.exit(1); });
