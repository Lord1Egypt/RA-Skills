## Description:

3GPP Scout provides semantic search over text, diagrams, and figures in the 3GPP TS/TR corpus from Rel-15 through Rel-20 via REST and hosted MCP interfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chriscarrotlabs](https://clawhub.ai/user/chriscarrotlabs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, standards engineers, and agents use this skill to search 3GPP TS/TR specifications, retrieve relevant sections, inspect figures, and compare standards content across releases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to fetch a mutable remote agent-setup prompt that was not included for review.

Mitigation: Review the remote prompt separately and do not let it authorize extra tools, files, domains, credentials, or workflow changes beyond 3GPP search setup.

Risk: Search queries are sent to the hosted 3GPP Scout service.

Mitigation: Use the skill only when sharing search queries with the service is acceptable, and avoid submitting confidential or sensitive material unless covered by the applicable agreement.

## Reference(s):

- [3GPP Scout Skill Page](https://clawhub.ai/chriscarrotlabs/skills/3gpp-scout)
- [3GPP Scout Homepage](https://3gppscout.com)
- [3GPP Scout API Docs](https://api.3gppscout.com/docs)
- [3GPP Scout Hosted MCP](https://api.3gppscout.com/mcp/)
- [3GPP Scout Agent Setup Prompt](https://api.3gppscout.com/agent-setup/prompt.md)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, API calls, text]

**Output Format:** [Markdown guidance with JSON request examples and shell environment snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [REST endpoints require SCOUT_API_KEY; hosted MCP uses OAuth 2.1.]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
