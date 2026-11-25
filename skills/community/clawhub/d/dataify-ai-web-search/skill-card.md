## Description:

Search web, shopping, news, or scholarly sources, with optional extraction of result content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to search web, news, shopping, and scholarly sources, optionally extracting content from result pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries may be sent to Dataify's external service.

Mitigation: Avoid sensitive queries and use the skill only where external search and extraction are permitted.

## Reference(s):

- [AI Web API search parameter contract](references/search-api.md)
- [AI Web API search endpoint](https://aiwebapi.dataify.com/search)
- [ClawHub release page](https://clawhub.ai/dataify-server/skills/dataify-ai-web-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Links]

**Output Format:** [Structured search results with optional extracted Markdown, raw HTML, clean HTML, or links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shopping and news result URLs may be redirects; snippets may be null.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
