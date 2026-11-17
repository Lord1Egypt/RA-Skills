## Description:

Enables AI agents to interact with AISP (Agent Inference Sharing Protocol) for renting or providing DIEM API capacity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daveo280](https://clawhub.ai/user/daveo280)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to rent DIEM/Venice inference capacity or list capped API keys through USDC escrow workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents toward real marketplace actions involving USDC escrow, wallet signing, fund transfers, settlement, and credential submission.

Mitigation: Require explicit user confirmation before wallet signing, fund transfers, settlement, or credential submission.

Risk: API keys used with the marketplace can expose more capability than intended if they are broad or long-lived.

Mitigation: Use scoped, revocable, inference-only API keys and verify backend and contract addresses before use.

## Reference(s):

- [ClawHub AISP skill page](https://clawhub.ai/daveo280/skills/aisp)
- [AISP homepage repository](https://github.com/DaveO280/Diem-Marketplace-V2-)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API endpoints, TypeScript examples, and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes wallet-signing, escrow, backend URL, and scoped API-key handling guidance.]

## Skill Version(s):

2.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
