## Description:

Helps autonomous agents self-register a first-class ~alter identity, check accrued Identity Income, and find licensed cash-out options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[true-alter](https://clawhub.ai/user/true-alter)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill when an autonomous agent needs to mint its own ~alter handle without a human account, then check earnings and cash-out options. It is also useful when a human explicitly asks their agent to set up its own identity and earnings path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The registration response returns an api_key that is shown once and can grant access to later authenticated ~alter calls.

Mitigation: Store the api_key immediately in a secure credential store, avoid exposing it in chat or logs, and rotate or re-register if it may have been exposed.

Risk: An agent may try to complete registration without code execution or may reuse an expired or single-use proof-of-work challenge.

Mitigation: Run a local solver using the returned difficulty value, submit the nonce before expiry, and request a fresh challenge if the previous one expires.

Risk: Users may expect wallet payout setup to be available through MCP, but the artifact states that payout wallet setup is a REST-only step with separate attestation requirements.

Mitigation: Use the skill for registration, earnings checks, and cash-out discovery, and handle payout wallet setup through the documented REST path or a human operator account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/true-alter/skills/alter-register-and-earn)
- [~alter MCP server](https://mcp.truealter.com/api/v1/mcp)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with Python and Node.js code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes MCP server configuration guidance, proof-of-work solver examples, and credential-handling guidance for ALTER_API_KEY.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
