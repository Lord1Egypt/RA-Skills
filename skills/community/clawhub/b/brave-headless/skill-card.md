## Description:

Headless Brave Browser provides Brave Search API web search and optional HTTP/HTTPS page content extraction as plain text, Markdown, or newline-delimited JSON without a browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelexine](https://clawhub.ai/user/kelexine)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to perform scriptable web research, documentation lookup, search-result collection, and URL content extraction from non-interactive environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary HTTP/HTTPS URLs from the agent's network environment.

Mitigation: Use it in a network-isolated environment or with egress controls, and avoid providing untrusted or private URLs.

Risk: The security summary notes weak response-size controls, especially when page content extraction is enabled.

Mitigation: Be cautious with --content and use conservative MAX_CONTENT_LENGTH or --max-length settings.

Risk: Dependency state may change over time for the Node.js packages used during extraction.

Mitigation: Update or review the dependency lockfile before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kelexine/skills/brave-headless)
- [Project Homepage](https://github.com/kelexine/brave-headless)
- [Brave Search API](https://brave.com/search/api)
- [Architecture Reference](artifact/ARCHITECTURE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Plain text, Markdown, or newline-delimited JSON from Node.js CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BRAVE_API_KEY; content extraction can be bounded with MAX_CONTENT_LENGTH or --max-length.]

## Skill Version(s):

0.2.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
