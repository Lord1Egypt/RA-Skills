## Description:

安全的网络搜索工具，支持多个搜索引擎。

This skill is ready for commercial/non-commercial use.

## Publisher:

[nidhov01](https://clawhub.ai/user/nidhov01)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to search the web through DuckDuckGo or Wikipedia, return summarized search results, and reuse cached results for repeated queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and returned snippets are cached locally in ~/.ai_search_cache.db.

Mitigation: Avoid sensitive queries unless local search history is acceptable, and clear the cache when retained search history is no longer needed.

Risk: Python dependencies are installed from version ranges and can change over time.

Mitigation: Install in a virtual environment and use pinned or locked dependencies for stronger supply-chain control.

Risk: Cached or external search results can be stale, incomplete, or inaccurate.

Mitigation: Verify important results against authoritative sources and clear the cache when current results are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nidhov01/skills/02)
- [Publisher profile](https://clawhub.ai/user/nidhov01)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Plain text and Markdown with Python snippets, shell commands, and structured search result fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results may be cached locally for 24 hours.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
