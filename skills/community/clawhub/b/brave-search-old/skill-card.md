## Description:

Web search and content extraction via Brave Search API. Use for searching documentation, facts, or any web content. Lightweight, no browser required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amabillis](https://clawhub.ai/user/amabillis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search the web, look up current information or documentation, and extract readable Markdown content from web pages without an interactive browser.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends searches to Brave and can fetch arbitrary web pages from the agent's network position without destination safeguards.

Mitigation: Use it only in environments where outbound network access is sandboxed or filtered, and avoid secrets, internal URLs, private services, and cloud metadata endpoints.

Risk: The security evidence reports that the Brave API disclosure does not match the implementation.

Mitigation: Confirm the expected Brave integration behavior and required credentials before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amabillis/skills/brave-search-old)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Plain text search results with optional Markdown page content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BRAVE_API_KEY setup according to the skill documentation; fetched page content is truncated by the script when included with search results.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
