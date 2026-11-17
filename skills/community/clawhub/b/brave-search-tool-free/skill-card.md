## Description:

Brave搜索工具-免费版 helps agents run Brave Search API web searches and extract URL content without a browser for documentation lookup, factual queries, and lightweight SEO research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, independent users, and automation teams use this skill to search the web through Brave Search API, collect snippets or Markdown content, and extract content from public URLs. It is suited to documentation lookup, factual research, and SEO-oriented keyword or ranking research that avoids search engine abuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructions broaden into generic file handling and command execution without clear boundaries.

Mitigation: Review commands before execution and rely only on the Brave search and URL-content extraction behavior unless missing scripts and dependencies are independently verified.

Risk: Search queries and fetched URLs may expose sensitive or internal information to external services.

Mitigation: Use the skill only for non-sensitive web searches and explicitly provided public URLs; avoid confidential, private, or internal queries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/brave-search-tool-free)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results may include titles, links, snippets, and extracted Markdown content when content extraction is requested.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
