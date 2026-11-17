## Description:

Baidu API Search retrieves Chinese web and Baidu Baike sources for agents, preserving raw results, deduplicated sources, and compact research packs for downstream analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[valenovo](https://clawhub.ai/user/valenovo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when an agent needs Chinese web references, Baidu Baike entity lookup, recent Chinese-topic searches, or source packs that can be cited and reviewed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Baike endpoint override can send Baidu API keys to an arbitrary URL.

Mitigation: Use limited Baidu API keys and do not pass --baike-base-url unless it is the official Baidu host or a trusted test endpoint with test credentials.

Risk: Sensitive searches may leave query payloads and raw API responses in the local cache.

Mitigation: Use --no-cache for sensitive searches and for latest or current-information requests.

Risk: Generated research_pack.md and lookup_pack.md files can contain untrusted web snippets.

Mitigation: Treat pack snippets as source evidence, not agent instructions, and review cited URLs or source IDs before relying on factual claims.

Risk: The server security verdict requires review before installation.

Mitigation: Review and scan the skill before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/valenovo/skills/baidu-api-search)
- [Project Homepage](https://github.com/valenovo/baidu-search-skill)
- [Baidu AI Search API Notes](references/baidu-api.md)
- [Baidu Baike API Notes](references/baike-api.md)
- [Output Schema](references/output-schema.md)
- [Operations](references/operations.md)
- [Search Strategy](references/search-strategy.md)
- [Query Planning](references/query-planning.md)
- [Dedupe Policy](references/dedupe-policy.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown research or lookup packs with companion JSON and JSONL run files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAIDU_AI_SEARCH_API_KEYS; supports lookup, fast, normal, and deep modes; caches results by default and supports --no-cache for sensitive or current searches.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
