## Description:

Universal Search-First Knowledge Acquisition Plugin for LLMs that enables real-time web search and deep page browsing via MCP or CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wd041216-bit](https://clawhub.ai/user/wd041216-bit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add live web search, page browsing, and source-cited retrieval behavior to LLM agents for current or factual questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages broad external web searches, which can expose sensitive query terms, internal URLs, or private document-derived context to external services.

Mitigation: Avoid enabling it for prompts containing secrets, proprietary information, internal URLs, or private documents unless derived queries and URLs are approved for external use.

Risk: The setup guidance installs an executable MCP server from an unpinned GitHub source.

Mitigation: Use a pinned and reviewed revision, install it in an isolated environment, and review the package before enabling it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wd041216-bit/skills/free-web-search-ultimate)
- [Homepage](https://github.com/wd041216-bit/free-web-search-ultimate)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source URLs, search queries, MCP setup snippets, and browsing guidance.]

## Skill Version(s):

11.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
