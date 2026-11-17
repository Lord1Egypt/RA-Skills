## Description:

Provides real-time package tracking across more than 1,300 carriers and merchant returns center demos through AfterShip, with fallback links when the MCP service is unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aftership](https://clawhub.ai/user/aftership)

### License/Terms of Use:

MIT-0

## Use Case:

External users and merchants use this skill to check shipment status, delivery events, and estimated delivery dates, or to preview an AfterShip Returns Center experience for a specific store domain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tracking numbers, carrier hints, or merchant store domains may be sent to AfterShip when the skill handles tracking or returns-demo requests.

Mitigation: Use the skill only when sharing those identifiers with AfterShip is acceptable, and review user prompts before invoking the remote MCP service.

Risk: Agent replies may include AfterShip-branded links with UTM parameters because the skill instructs agents to preserve those links verbatim.

Mitigation: Review generated replies before sending them in contexts where branded links or UTM parameters are not desired.

Risk: The skill depends on a live remote MCP endpoint for tracking and returns-demo data.

Mitigation: Use the documented fallback links when the MCP endpoint is unavailable, and avoid silent failures.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aftership/skills/aftership-tracking-and-returns)
- [AfterShip](https://www.aftership.com)
- [AfterShip MCP Endpoint](https://mcp.aftership.com/tracking/public)
- [AfterShip Privacy Policy](https://www.aftership.com/legal/privacy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with links, inline commands, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include AfterShip-branded tracking or demo URLs returned by the connected service.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
