#!/usr/bin/env node
// ⚠️ DO NOT EDIT — auto-generated from sdks/_shared/scripts/lookup.js
// Edit the source in sdks/_shared/scripts/ then run:
//   bash scripts/sync-shared-scripts.sh
// See docs/features/f-036/shared-scripts-consolidation.md

// ---------------------------------------------------------------------------
// awareness_lookup — Fast structured DB queries (no vector search)
// Usage: node lookup.js type=tasks [status=pending] [priority=high] [limit=50]
//        node lookup.js type=knowledge [query=auth] [category=architecture]
//        node lookup.js type=risks [level=high] [status=active]
//        node lookup.js type=timeline [limit=20] [session_id=xxx]
//        node lookup.js type=context [days=7]
//        node lookup.js type=handoff [query="continue auth work"]
//        node lookup.js type=rules [format=markdown]
//        node lookup.js type=graph [entity_id=xxx] [search=auth]
//        node lookup.js type=agents
//        node lookup.js type=skills [query=auth] [category=skill] [status=active]
// ---------------------------------------------------------------------------

const { loadConfig, resolveEndpoint, mcpCall, apiGet, parseArgs } = require("./shared");

async function main() {
  const args = parseArgs();
  const type = args.type;
  if (!type) {
    console.log(JSON.stringify({ error: "Usage: node lookup.js type=<type> [params...]", types: [
      "context", "tasks", "knowledge", "risks", "timeline", "session_history", "handoff", "rules", "graph", "agents", "skills"
    ]}));
    return;
  }

  const config = loadConfig();
  const ep = await resolveEndpoint(config);
  if (!ep) { console.log(JSON.stringify({ error: "Not configured." })); return; }

  if (ep.mode === "local") {
    // Local daemon: use MCP awareness_lookup
    const mcpArgs = { type };
    if (args.status) mcpArgs.status = args.status;
    if (args.priority) mcpArgs.priority = args.priority;
    if (args.limit) mcpArgs.limit = Number(args.limit);
    if (args.query) mcpArgs.query = args.query;
    if (args.category) mcpArgs.category = args.category;
    if (args.level) mcpArgs.level = args.level;
    if (args.session_id) mcpArgs.session_id = args.session_id;
    if (args.entity_id) mcpArgs.entity_id = args.entity_id;
    if (args.search) mcpArgs.search = args.search;
    if (args.format) mcpArgs.format = args.format;
    if (args.days) mcpArgs.days = Number(args.days);

    const result = await mcpCall(ep.localUrl, "awareness_lookup", mcpArgs);
    console.log(typeof result === "string" ? result : JSON.stringify(result, null, 2));
    return;
  }

  // Cloud: use REST API
  const params = new URLSearchParams();
  if (config.agentRole) params.set("agent_role", config.agentRole);

  let result;

  switch (type) {
    case "context": {
      if (args.days) params.set("days", String(args.days));
      if (args.max_cards) params.set("max_cards", String(args.max_cards));
      if (args.max_tasks) params.set("max_tasks", String(args.max_tasks));
      result = await apiGet(ep.baseUrl, ep.apiKey, `/memories/${ep.memoryId}/context`, params);
      break;
    }
    case "tasks": {
      if (args.status) params.set("status", args.status);
      if (args.priority) params.set("priority", args.priority);
      if (args.limit) params.set("limit", String(args.limit));
      result = await apiGet(ep.baseUrl, ep.apiKey, `/memories/${ep.memoryId}/insights/action-items`, params);
      break;
    }
    case "knowledge": {
      if (args.query) params.set("query", args.query);
      if (args.category) params.set("category", args.category);
      if (args.limit) params.set("limit", String(args.limit));
      result = await apiGet(ep.baseUrl, ep.apiKey, `/memories/${ep.memoryId}/insights/knowledge-cards`, params);
      break;
    }
    case "risks": {
      if (args.level) params.set("level", args.level);
      if (args.status) params.set("status", args.status);
      if (args.limit) params.set("limit", String(args.limit));
      result = await apiGet(ep.baseUrl, ep.apiKey, `/memories/${ep.memoryId}/insights/risks`, params);
      break;
    }
    case "timeline": {
      if (args.limit) params.set("limit", String(args.limit));
      if (args.offset) params.set("offset", String(args.offset));
      if (args.session_id) params.set("session_id", args.session_id);
      params.set("include_summaries", "true");
      result = await apiGet(ep.baseUrl, ep.apiKey, `/memories/${ep.memoryId}/timeline`, params);
      break;
    }
    case "session_history": {
      if (!args.session_id) { console.log(JSON.stringify({ error: "session_id required" })); return; }
      params.set("session_id", args.session_id);
      if (args.limit) params.set("limit", String(args.limit));
      result = await apiGet(ep.baseUrl, ep.apiKey, `/memories/${ep.memoryId}/content`, params);
      break;
    }
    case "handoff": {
      params.set("days", "3");
      params.set("max_cards", "5");
      params.set("max_tasks", "10");
      result = await apiGet(ep.baseUrl, ep.apiKey, `/memories/${ep.memoryId}/context`, params);
      break;
    }
    case "rules": {
      if (args.format) params.set("format", args.format);
      result = await apiGet(ep.baseUrl, ep.apiKey, `/memories/${ep.memoryId}/rules`, params);
      break;
    }
    case "graph": {
      if (args.limit) params.set("limit", String(args.limit));
      if (args.entity_type) params.set("entity_type", args.entity_type);
      if (args.search) params.set("search", args.search);
      const graphPath = args.entity_id
        ? `/memories/${ep.memoryId}/graph/entities/${args.entity_id}/neighbors`
        : `/memories/${ep.memoryId}/graph/entities`;
      result = await apiGet(ep.baseUrl, ep.apiKey, graphPath, params);
      break;
    }
    case "agents": {
      result = await apiGet(ep.baseUrl, ep.apiKey, `/memories/${ep.memoryId}/agents`, params);
      break;
    }
    case "skills": {
      if (args.query) params.set("query", args.query);
      if (args.category) params.set("category", args.category);
      if (args.status) params.set("status", args.status);
      if (args.limit) params.set("limit", String(args.limit));
      result = await apiGet(ep.baseUrl, ep.apiKey, `/memories/${ep.memoryId}/skills`, params);
      break;
    }
    default:
      console.log(JSON.stringify({ error: `Unknown type: ${type}` }));
      return;
  }

  console.log(JSON.stringify(result, null, 2));
}

main().catch(e => { console.error(`[awareness] lookup failed: ${e.message}`); process.exit(1); });
