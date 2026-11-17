## Description:

Enrich company, person, and contact data with 25 tools via the Enrich Layer API. Look up companies, find decision-makers, get work emails, search employees, verify contacts, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicest-michael](https://clawhub.ai/user/nicest-michael)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to enrich company, person, contact, school, and job records through the Enrich Layer API. It supports credit-aware lookup, search, verification, and profile-enrichment workflows for professional-network data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned npm MCP server with an Enrich Layer API key.

Mitigation: Pin the MCP package to a reviewed exact version and limit the process environment to ENRICH_LAYER_API_KEY only.

Risk: Personal email and phone lookup tools can expose or process personal contact data.

Mitigation: Use personal contact lookup only with proper authorization, purpose limitation, and applicable privacy-law compliance.

Risk: Bulk enrichment, employee lists, and people searches can consume paid Enrich Layer credits.

Mitigation: Check credit balance before large operations and warn users about estimated credit cost before running them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nicest-michael/skills/enrich-layer)
- [Enrich Layer Homepage](https://enrichlayer.com)
- [Enrich Layer API Docs](https://enrichlayer.com/docs)
- [Enrich Layer Dashboard](https://enrichlayer.com/dashboard)
- [npm Package](https://www.npmjs.com/package/@verticalint-michael/enrich-layer-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown or structured text with optional shell commands, JSON configuration snippets, and MCP tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and ENRICH_LAYER_API_KEY; many workflows consume Enrich Layer credits.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
