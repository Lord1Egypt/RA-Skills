## Description:

Extract Markdown, raw HTML, clean HTML, or links from a specified public webpage, with controls for content filtering, timeouts, and wait conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to retrieve selected content from a public webpage as Markdown, HTML, or links, with optional controls for filtering and page loading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security guidance notes network and environment capabilities without a declared tool scope.

Mitigation: Use only intended public URLs, review any custom headers, and keep DATAIFY_API_TOKEN private in the environment.

## Reference(s):

- [AI Web API Extract parameter contract](references/extract-api.md)
- [AI Web API /extract endpoint](https://aiwebapi.dataify.com/extract)
- [ClawHub skill release](https://clawhub.ai/dataify-server/skills/dataify-ai-web-extract)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Links]

**Output Format:** [JSON API response containing the requested extraction output or outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The API returns outputs keyed by requested format; successful uncached extractions incur one gateway tool unit charge.]

## Skill Version(s):

1.0.2 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
