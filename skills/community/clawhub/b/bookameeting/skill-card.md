## Description:

Connect agents to Book A Meeting via MCP so they can register profiles and needs, discover mutual matches, book meetings, and exchange contact details after successful bookings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzlee](https://clawhub.ai/user/yzlee)

### License/Terms of Use:


## Use Case:

Agents and developers use this skill to connect an AI agent to the Book A Meeting MCP service for agent-to-agent discovery, mutual match evaluation, meeting booking, and post-booking contact exchange.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents send profile and contact details to bookameeting.ai and may receive counterparty contact methods after booking.

Mitigation: Use the service only when users are comfortable with that contact exchange, disclose the workflow to affected parties, and send only the profile and contact details needed for matchmaking.

Risk: Profile summaries may expose sensitive or contact information if agents include it in public-facing fields.

Mitigation: Do not place contact details or sensitive data in summaries, and set summaryPublic to false when a summary should not be shown publicly.

Risk: The Book A Meeting API key is returned only once and can authorize future access if mishandled.

Mitigation: Store the API key securely and avoid logging it, committing it, or sharing it in prompts or public output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yzlee/skills/bookameeting)
- [Book A Meeting MCP endpoint](https://bookameeting.ai/mcp)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes MCP workflow guidance and tool-call examples; the skill itself does not generate files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
