#!/usr/bin/env node
// ⚠️ DO NOT EDIT — auto-generated from sdks/_shared/scripts/search.js
// Edit the source in sdks/_shared/scripts/ then run:
//   bash scripts/sync-shared-scripts.sh
// See docs/features/f-036/shared-scripts-consolidation.md

// ---------------------------------------------------------------------------
// awareness_recall — Semantic + keyword hybrid search
// Usage: node search.js "query text" [keyword_query="terms"] [limit=6]
//        [scope=all|timeline|knowledge|insights] [recall_mode=hybrid]
//        [vector_weight=0.7] [bm25_weight=0.3]
//        [multi_level=true] [cluster_expand=true]
//        [detail=summary|full] [ids=id1,id2]
// ---------------------------------------------------------------------------

const { loadConfig, resolveEndpoint, mcpCall, apiPost, parseArgs } = require("./shared");

async function main() {
  const args = parseArgs();
  const query = args.query;
  if (!query) { console.log(JSON.stringify({ error: "Usage: node search.js \"query\" [options]" })); return; }

  const config = loadConfig();
  const ep = await resolveEndpoint(config);
  if (!ep) { console.log(JSON.stringify({ error: "Not configured." })); return; }

  if (ep.mode === "local") {
    // Local daemon: use MCP JSON-RPC
    const mcpArgs = {
      semantic_query: query,
      detail: args.detail || "summary",
      limit: Math.max(1, Math.min(Number(args.limit) || 6, 30)),
    };
    if (args.keyword_query) mcpArgs.keyword_query = args.keyword_query;
    if (args.ids) mcpArgs.ids = String(args.ids).split(",");
    const result = await mcpCall(ep.localUrl, "awareness_recall", mcpArgs);
    if (typeof result === "string") {
      // MCP returns human-readable text for recall
      console.log(result);
    } else {
      console.log(JSON.stringify(result, null, 2));
    }
  } else {
    // Cloud: use REST API
    const customKwargs = {
      limit: Math.max(1, Math.min(Number(args.limit) || 6, 30)),
      use_hybrid_search: true,
      reconstruct_chunks: true,
      vector_weight: Number(args.vector_weight) || 0.7,
      bm25_weight: Number(args.bm25_weight) || 0.3,
    };

    if (args.multi_level) customKwargs.multi_level = true;
    if (args.cluster_expand) customKwargs.cluster_expand = true;

    // Scope filter
    if (args.scope && args.scope !== "all") {
      const scopeMap = {
        timeline: ["timeline"],
        knowledge: ["knowledge", "full_source"],
        insights: ["insight_summary"],
      };
      if (scopeMap[args.scope]) customKwargs.metadata_filter = { aw_content_scope: scopeMap[args.scope] };
    }

    const body = {
      query,
      recall_mode: args.recall_mode || "hybrid",
      custom_kwargs: customKwargs,
      include_installed: true,
    };
    if (args.keyword_query) body.keyword_query = args.keyword_query;
    if (config.agentRole) body.agent_role = config.agentRole;
    if (args.detail) body.detail = args.detail;
    if (args.ids) body.ids = String(args.ids).split(",");
    if (args.user_id) body.user_id = args.user_id;
    if (args.confidence_threshold) body.confidence_threshold = Number(args.confidence_threshold);

    const result = await apiPost(ep.baseUrl, ep.apiKey, `/memories/${ep.memoryId}/retrieve`, body);
    console.log(JSON.stringify(result, null, 2));
  }
}

main().catch(e => { console.error(`[awareness] search failed: ${e.message}`); process.exit(1); });
