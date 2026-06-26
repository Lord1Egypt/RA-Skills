## Description: <br>
Baidu API Search is a source-retrieval skill for AI agents that need Chinese web references from Baidu AI Search and Baidu Baike. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[valenovo](https://clawhub.ai/user/valenovo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to search Chinese web sources, perform lightweight Baidu Baike entity lookups, deduplicate results, and prepare cited research packs for downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search topics and related query text are sent to Baidu APIs. <br>
Mitigation: Use the skill only for topics suitable for Baidu processing, and avoid sending confidential or regulated data unless that use has been approved. <br>
Risk: The skill requires a Baidu AI Search/AppBuilder API key and may consume quota or incur account costs. <br>
Mitigation: Use a dedicated key, keep it in BAIDU_AI_SEARCH_API_KEYS, monitor quota or billing, and do not store or print the key. <br>
Risk: Run outputs and caches can retain queries, raw results, and research packs on disk. <br>
Mitigation: Use --no-cache for sensitive or current searches, and clear local runs and cache directories when retained search data should not remain. <br>
Risk: Cached results can be stale for latest or current-information requests. <br>
Mitigation: Use --no-cache and freshness filters for recent or current searches, then cite source IDs or URLs from the generated packs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/valenovo/baidu-api-search) <br>
- [Publisher profile](https://clawhub.ai/user/valenovo) <br>
- [Homepage](https://github.com/valenovo/baidu-search-skill) <br>
- [Baidu AI Search API Notes](references/baidu-api.md) <br>
- [Baidu Baike API Notes](references/baike-api.md) <br>
- [Output Schema](references/output-schema.md) <br>
- [Operations](references/operations.md) <br>
- [Dedupe Policy](references/dedupe-policy.md) <br>
- [Query Planning](references/query-planning.md) <br>
- [Search Strategy](references/search-strategy.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown research or lookup packs plus JSON and JSONL run artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes run directories containing query plans, raw results, deduplicated sources, summaries, optional error logs, and cache-aware trace files.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
