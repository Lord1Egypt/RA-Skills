# Shared Retrieval Domain Pack — LLM Agents

## Purpose

This domain pack externalizes the LLM-agent-specific pinned IDs, topic detection,
and query construction logic that was previously hardcoded in:
- `arxiv-search/scripts/run.py` (`_looks_like_llm_agent_topic`, `_llm_agent_query`)
- `literature-engineer/scripts/run.py` (`_pinned_arxiv_ids`)
- `dedupe-rank/scripts/run.py` (`_looks_like_llm_agent_topic`, `_pinned_records`, `_is_agent_survey_record`)

## Loading

All three retrieval skills should load:
```
assets/domain_packs/llm_agents.json
```

If the workspace topic does NOT match any domain pack's `topic_triggers`, the skills
should fall back to generic behavior (no pinning, no query rewriting, no survey boosting).

## How to Add a New Domain

1. Create a new JSON file under `assets/domain_packs/` (e.g., `robotics.json`)
2. Fill in `topic_triggers`, `pinned_classics`, `pinned_surveys`, `query_rewrite_rules`, and `survey_detection`
3. No code changes needed — the scripts load all packs and match by trigger
