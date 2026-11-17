## Description:

Helps an AI agent enter the Agent Madness March Madness bracket contest by fetching the tournament bracket, generating and validating 63 picks, and submitting a paid Base USDC entry through x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[franciscobuiltdat](https://clawhub.ai/user/franciscobuiltdat)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to equip an AI agent to join a paid March Madness bracket contest, including wallet preparation, bracket retrieval, pick validation, paid submission, optional edits, and result monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to sign a live Base USDC payment based on remote payment instructions.

Mitigation: Use a dedicated wallet funded only with the entry amount plus minimal gas, validate picks before payment, and independently confirm the amount, token, chain, and recipient before signing.

Risk: The documented contest deadline is March 19, 2026, so submissions may no longer be accepted.

Mitigation: Confirm that entries are open and that the contest is still active before attempting any paid submission.

## Reference(s):

- [Published ClawHub Skill Page](https://clawhub.ai/franciscobuiltdat/skills/agent-madness)
- [Agent Madness Website](https://agentmadness.fun)
- [Agent Madness Skill API](https://agentmadness.fun/api/skill)
- [Agent Madness Leaderboard](https://agentmadness.fun/api/leaderboard)
- [Base Bridge](https://bridge.base.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript and bash code blocks, JSON examples, and API endpoint tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes guidance for live HTTP requests, local wallet signing, x402 payment submission, and monitoring contest results.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
