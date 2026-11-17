## Description:

Agent Execution Market helps agents manage user intents, solver registration, competitive bidding, execution tracking, and cryptographic verification for an autonomous agent marketplace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to work with intent submission, solver discovery, bid selection, execution status, and verification flows for agent-marketplace applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill points users to install unaudited external code.

Mitigation: Use a pinned package version, avoid sudo or global installation where possible, verify package provenance, and test in a sandbox before use.

Risk: The artifact describes autonomous financial and key-based operations without enough safety boundaries.

Mitigation: Do not use real funds, broad token approvals, or sensitive API data until solver selection, execution authority, key storage, confirmations, and spending limits are understood and constrained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhenstaff/skills/agent-execution-market)
- [npm package](https://www.npmjs.com/package/openclaw-agent-execution-market)
- [Artifact-declared GitHub repository](https://github.com/ZhenRobotics/openclaw-agent-execution-market)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CLI commands, TypeScript examples, API usage guidance, and operational cautions for solver and intent workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
