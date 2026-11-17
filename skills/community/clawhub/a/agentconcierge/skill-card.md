## Description:

Find and recommend AI agents for any workflow using AgentConcierge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gomisterb](https://clawhub.ai/user/gomisterb)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use this skill to find AI agents for a role, task, pain point, budget, tool stack, or team context. The skill queries AgentConcierge and returns ranked recommendations with match scores and reasons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workflow context is sent to the external AgentConcierge service for recommendations.

Mitigation: Collect only the role and pain point required for the request, and avoid sending secrets, credentials, regulated personal data, or confidential internal project details.

Risk: The skill depends on network access to agentconcierge.io and may be rate-limited.

Mitigation: Handle 429 responses by waiting before retrying, and direct users to the AgentConcierge search page when the API is unavailable.

## Reference(s):

- [AgentConcierge API Reference](references/api-schema.md)
- [AgentConcierge](https://agentconcierge.io)
- [AgentConcierge Search](https://agentconcierge.io/search)
- [AgentConcierge Developer API](https://agentconcierge.io/developers)
- [ClawHub Skill Page](https://clawhub.ai/gomisterb/skills/agentconcierge)
- [ClawHub Publisher Profile](https://clawhub.ai/user/gomisterb)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown recommendations backed by a JSON API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns five ranked AI agent recommendations with match scores, reasons, pricing, and URLs when available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
