---
name: cross_check
description: "Multi-source verification with confidence ratings. Use for verifying factual claims, finding examples and verifying they match criteria, statistics, or research requiring cross-checking. Also triggers on 'find X and verify' discovery tasks. Triggers: verify, cross-check, find and verify, 驗證, 查證, 核實, 尋找, 搵."
homepage: https://github.com/marianachow0321/openclaw-skill-cross-check
metadata: { "clawdbot": { "emoji": "🔍", "requires": { "env": [] }, "files": ["references/*"] } }
---

# Cross Check

Multi-source verification for factual claims with confidence scoring and source links.

## Workflow

1. **Optimize query** — see `{baseDir}/references/query-optimization.md`.
2. **Search first (REQUIRED)** — ALWAYS use `web_search` as the primary tool. Never skip to `web_fetch` directly. Run `web_search(query, count=10)`. If T1 found, stop. If only T2-3, run a second query. If contradictions, investigate.
3. **Evaluate sources** — classify by tier. See `{baseDir}/references/source-tiers.md`.
4. **Direct verify** (optional, only after search) — use `web_fetch(url)` only to verify specific URLs found via search. Never use `web_fetch` as a substitute for `web_search`.
5. **Present** — MUST include clickable source URLs for every result:
   > [Answer]
   > Confidence: [T1-T5] ([%]) | Sources: [name](url), ... | Verified: [date] | Note: [caveats]

## Source URLs

CRITICAL: Every cited source MUST include a direct clickable URL. If URL unavailable: T1 → find alternative source, T2+ → downgrade one tier. Never list a source without its URL.

## Error Handling

- Zero results → broaden query, retry once. Still empty → T1 confidence.
- `web_fetch` fails → skip, note it, drop confidence one level.
- All T4 sources → report T2, mark Uncertain.
- Contradictions → see `{baseDir}/references/research-patterns.md`.

## Security & Privacy

This skill uses only OpenClaw's built-in `web_search` and `web_fetch` tools. No data is sent to external services beyond what these tools do.

**External Endpoints:**
- Web search API (via OpenClaw's built-in web_search, provider depends on user config)
- Web pages (via OpenClaw's web_fetch for verification)

**Data Handling:**
- No credentials required
- No data stored locally
- Search queries sent through OpenClaw's configured search provider
- No autonomous invocation without user intent - activates when queries contain verification language

**Trust Statement:**
By using this skill, your search queries are sent through OpenClaw's built-in web search provider. Only install if you trust OpenClaw's data handling practices.
