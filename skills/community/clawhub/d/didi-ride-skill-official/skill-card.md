## Description:

DiDi Ride SKILL lets an OpenClaw agent use DiDi MCP tools for ride hailing, order status, driver location, cancellation, route planning, and nearby search in supported Mainland China cities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[didi](https://clawhub.ai/user/didi)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill through an agent to request DiDi rides, compare route and fare options, query active orders, cancel rides after confirmation, and manage ride preferences.

### Deployment Geography for Use:

Mainland China cities served by DiDi; not available in Hong Kong, Macau, Taiwan, or outside China.

## Known Risks and Mitigations:

Risk: The skill requires a DiDi MCP key and can persist that credential.

Mitigation: Use a secure key setup path, avoid pasting keys into shared logs, and rotate any key exposed in chat or logs.

Risk: The skill can create real ride orders and scheduled background tasks.

Mitigation: Require explicit user confirmation before dispatching, canceling, or scheduling rides.

Risk: The skill can store local ride preferences such as addresses and phone numbers.

Mitigation: Store only necessary preference data and review local preference files before sharing or publishing the workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/didi/skills/didi-ride-skill-official)
- [DiDi MCP platform](https://mcp.didichuxing.com/claw)
- [README.en.md](README.en.md)
- [Setup guide](references/setup.md)
- [Workflow reference](references/workflow.md)
- [API references](references/api_references.md)
- [Error handling guide](references/error_handling.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured ride or route status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May issue MCP tool calls through mcporter and may update local ride preference files when the user asks to save preferences.]

## Skill Version(s):

1.1.3 (source: package.json, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
