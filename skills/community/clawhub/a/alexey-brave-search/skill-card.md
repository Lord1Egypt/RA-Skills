## Description:

Web search and content extraction via Brave Search API. Use for searching documentation, facts, or any web content. Lightweight, no browser required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexeyvorobiev](https://clawhub.ai/user/alexeyvorobiev)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to search the web, look up documentation or current facts, and extract readable page content as markdown without launching a browser.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Brave, and evidence.security reports that the skill scrapes Brave result pages rather than using the advertised API.

Mitigation: Use only for queries appropriate to send to Brave, disclose this behavior to users, and expect result parsing to require review if Brave changes its page structure.

Risk: The skill can fetch arbitrary web pages from the agent's network context.

Mitigation: Run it with outbound network controls and avoid environments that can reach private admin services, cloud metadata endpoints, or sensitive internal sites.

Risk: evidence.security reports that the release materially under-discloses how searches and content fetching are performed.

Mitigation: Review the skill before deployment and document its network behavior for operators and users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexeyvorobiev/skills/alexey-brave-search)
- [Brave Search](https://search.brave.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text search results with optional Markdown page extracts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include title, link, snippet, and optional extracted content; standalone content extraction returns readable Markdown.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
