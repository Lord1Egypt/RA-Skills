## Description:

Before connecting to an MCP, A2A or x402 server somebody handed you, check whether it answers, which of its tools actually respond when called, what they charge, whether its card tries to instruct you, and what changed since the last look.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brick-blue](https://clawhub.ai/user/brick-blue)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill before connecting to an MCP, A2A, or x402 server to check availability, tool response status, quoted prices, card instructions, and schema changes. It helps decide whether to connect, authenticate, pay, or inspect a server more carefully.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Endpoint URLs submitted for verification are shared with brick.blue, and fresh verification can trigger live calls from brick.blue to the target server.

Mitigation: Avoid submitting private or sensitive internal endpoints unless that disclosure and probing behavior is acceptable.

Risk: The skill reports verification evidence but does not connect, install, pay, or guarantee that a server remains unchanged after verification.

Mitigation: Treat verification results as point-in-time evidence and re-check with a fresh query before higher-risk connections or payments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brick-blue/skills/brick-blue-verify)
- [brick.blue verification API](https://brick.blue/api/v1/verify?url=<address>)
- [brick.blue MCP endpoint](https://brick.blue/mcp)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include verification status, tool verdicts, price information, card-signal warnings, schema-change notes, and receipt links.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
