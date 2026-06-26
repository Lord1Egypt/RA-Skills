#!/usr/bin/env node
// ---------------------------------------------------------------------------
// awareness_init — Initialize session and load cross-session context
// Usage: node init.js [days=7] [max_cards=20] [max_tasks=20]
// ---------------------------------------------------------------------------

const { loadConfig, resolveEndpoint, getSessionId, apiGet } = require("./shared");

async function main() {
  const { parseArgs } = require("./shared");
  const args = parseArgs();

  const config = loadConfig();
  const ep = await resolveEndpoint(config);
  if (!ep) { console.log(JSON.stringify({ error: "Not configured. Set AWARENESS_API_KEY and AWARENESS_MEMORY_ID." })); return; }

  const params = new URLSearchParams();
  params.set("days", String(args.days || 7));
  params.set("max_cards", String(args.max_cards || 20));
  params.set("max_tasks", String(args.max_tasks || 20));
  if (config.agentRole) params.set("agent_role", config.agentRole);

  const ctx = await apiGet(ep.baseUrl, ep.apiKey, `/memories/${ep.memoryId}/context`, params);
  const sessionId = getSessionId();

  console.log(JSON.stringify({
    session_id: sessionId,
    memory_id: ep.memoryId,
    last_sessions: ctx.last_sessions || [],
    recent_days: ctx.recent_days || [],
    open_tasks: ctx.open_tasks || [],
    knowledge_cards: ctx.knowledge_cards || [],
    active_skills: ctx.active_skills || [],
    attention_summary: ctx.attention_summary || null,
  }, null, 2));
}

main().catch(e => { console.error(`[awareness] init failed: ${e.message}`); process.exit(1); });
