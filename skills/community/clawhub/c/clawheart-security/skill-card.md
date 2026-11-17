## Description:

ClawHeart Security lets an AI agent drive the local ClawHeart CLI for AI security scans, skill audits, agent discovery, MCP listings, and provider configuration reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tjsdyy](https://clawhub.ai/user/tjsdyy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and AI governance teams use this skill to invoke local ClawHeart checks and summarize AI security, skill, agent, MCP, and provider configuration findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install fallback suggests executing remote installer scripts directly.

Mitigation: Independently verify and trust the installer source before running curl|sh or iwr|iex commands.

Risk: The skill can expose or modify sensitive local agent, MCP, provider, and credential-governance configuration.

Mitigation: Treat outputs as sensitive and require explicit user confirmation before listing or changing provider configuration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tjsdyy/skills/clawheart-security)
- [ClawHeart Website](https://clawheart.live)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text summaries derived from ClawHeart JSON output, with inline shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize sensitive local agent, MCP, provider, and credential-governance information.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
