## Description:

Cost Governor helps agents and operators track LLM API costs, enforce budget limits with circuit breakers, and manage optional x402-based Pro payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atlaspa](https://clawhub.ai/user/atlaspa)

### License/Terms of Use:

MIT License

## Use Case:

Developers, agent operators, and OpenClaw users use this skill to monitor LLM provider spend, receive budget alerts, pause activity at limits, and review cost reports before costs overrun budgets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous x402 payment setup can expose funds or allow payments without adequate operator review.

Mitigation: Use the free local tracking features unless payment is needed; isolate payment capability behind a dedicated low-balance wallet, hard signer limits, and explicit human approval.

Risk: The security review warns against running an unpinned npm setup in sensitive environments without verified package provenance and implementation.

Mitigation: Pin package versions, verify package provenance and reviewed source code, and run setup in an isolated environment before production use.

Risk: The artifact states the MVP payment verification trusts reported transaction hashes.

Mitigation: Do not rely on Pro payment enforcement until on-chain verification is implemented or independently validated.

## Reference(s):

- [Cost Governor ClawHub listing](https://clawhub.ai/atlaspa/skills/cost-governor)
- [x402 Protocol](https://www.x402.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands, JSON configuration examples, and HTTP request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce setup, status, dashboard, reporting, reset, and payment workflow guidance for local OpenClaw use.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
