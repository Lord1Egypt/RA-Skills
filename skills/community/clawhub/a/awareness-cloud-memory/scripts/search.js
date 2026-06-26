#!/usr/bin/env node
// ---------------------------------------------------------------------------
// awareness_recall — Semantic + keyword hybrid search
// Usage: node search.js "query text" [keyword_query="terms"] [limit=6]
//        [scope=all|timeline|knowledge|insights] [recall_mode=hybrid]
//        [vector_weight=0.7] [full_text_weight=0.3]
//        [multi_level=true] [cluster_expand=true]
//        [detail=summary|full] [ids=id1,id2]
// ---------------------------------------------------------------------------

const { loadConfig, resolveEndpoint, apiPost, parseArgs } = require("./shared");

async function main() {
  const args = parseArgs();
  const query = args.query;
  if (!query) { console.log(JSON.stringify({ error: "Usage: node search.js \"query\" [options]" })); return; }

  const config = loadConfig();
  const ep = await resolveEndpoint(config);
  if (!ep) { console.log(JSON.stringify({ error: "Not configured." })); return; }

  const customKwargs = {
    limit: Math.max(1, Math.min(Number(args.limit) || 6, 30)),
    use_hybrid_search: true,
    reconstruct_chunks: true,
    recall_mode: args.recall_mode || "hybrid",
    vector_weight: Number(args.vector_weight) || 0.7,
    full_text_weight: Number(args.full_text_weight) || 0.3,
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

  const body = { query, custom_kwargs: customKwargs, include_installed: true };
  if (args.keyword_query) body.keyword_query = args.keyword_query;
  if (config.agentRole) body.agent_role = config.agentRole;
  if (args.detail) body.detail = args.detail;
  if (args.ids) body.ids = String(args.ids).split(",");
  if (args.user_id) body.user_id = args.user_id;
  if (args.confidence_threshold) body.confidence_threshold = Number(args.confidence_threshold);

  const result = await apiPost(ep.baseUrl, ep.apiKey, `/memories/${ep.memoryId}/retrieve`, body);
  console.log(JSON.stringify(result, null, 2));
}

main().catch(e => { console.error(`[awareness] search failed: ${e.message}`); process.exit(1); });
