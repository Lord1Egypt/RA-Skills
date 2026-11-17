## Description:

百炼搜索工具-免费版 helps agents run AI-optimized web searches through the Bailian API and return concise multi-source results for personal developers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent builders use this skill to run web searches for facts, keyword research, SEO analysis, and early topic research, then pass concise multi-source results into downstream agent responses. The artifact states it is not suited for black-hat SEO, search-engine manipulation, or paid ad management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell and write-style authority may allow commands or local file operations beyond basic searching.

Mitigation: Review the skill before installation and run only the specific search commands needed in a constrained workspace.

Risk: Search queries, cached results, and saved research files can expose confidential or regulated topics on disk.

Mitigation: Use the skill only for non-sensitive web search or keyword research, and avoid saving or caching confidential queries or results.

Risk: The artifact gives broad examples for creating, deleting, saving, and caching data.

Mitigation: Treat file-modifying examples as optional and require explicit user confirmation before executing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/bailian-search-tool-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and plain-text search result output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search result count is configurable in the artifact from 1 to 20 results.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
