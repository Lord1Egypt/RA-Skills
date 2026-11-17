## Description:

Guides agents in obtaining Western and Vedic astrology charts, horoscopes, and compatibility reports through the Astro Agents service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aidatatools-dev](https://clawhub.ai/user/aidatatools-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to request birth charts, planetary positions, Vedic reports, and relationship compatibility readings from an astrology service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Birth date, time, and location are sent to a third-party astrology service.

Mitigation: Confirm the user is comfortable sharing those details before making a request.

Risk: Setup adds a persistent connection to the third-party MCP server.

Mitigation: Review and approve the server connection before installing the skill.

Risk: Free calls are limited and subsequent requests may require payment.

Mitigation: Tell the user when the limit is reached and obtain approval before any paid request.

## Reference(s):

- [Astrology skill on ClawHub](https://clawhub.ai/aidatatools-dev/skills/astrology)
- [Astro Agents MCP service](https://astro-agent.dev/mcp)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with setup instructions and astrology results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include a verification hash; charts with unknown birth times cannot reliably determine houses or the ascendant.]

## Skill Version(s):

1.1.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
