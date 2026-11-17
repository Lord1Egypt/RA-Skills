## Description:

Email service for AI agents with wallet authentication and crypto payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patrickshuff](https://clawhub.ai/user/patrickshuff)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to give AI agents a clawmail.xyz email inbox, authenticate with an Ethereum wallet, and manage messages through MCP or REST APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs or runs the npm package clawmail without a pinned version.

Mitigation: Pin and review the package version before use, and run it in a low-privilege environment.

Risk: The skill handles wallet signatures, session tokens, message reading, and message deletion.

Mitigation: Avoid exposing unrelated wallet or credential data and require explicit confirmation before deleting messages.

## Reference(s):

- [ClawMail homepage](https://clawmail.xyz)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports mailbox availability checks, wallet login, listing messages, reading messages, and deleting messages through MCP-style tools.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
