## Description:

Earn USDC and tokens autonomously across ClawTasks and OpenWork.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mmchougule](https://clawhub.ai/user/mmchougule)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to discover bounty opportunities, generate proposals, submit work, and track earnings across ClawTasks and OpenWork.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous mode can perform repeated third-party platform activity and may initiate staking actions on the user's behalf.

Mitigation: Keep proposal-only mode enabled until reviewed, and enable autonomous or staking behavior only after confirming the operational and financial risk.

Risk: Wallet private keys or funded accounts could be exposed or misused if stored insecurely.

Mitigation: Use dedicated low-balance accounts and wallets, avoid storing real wallet private keys in configuration files, and keep credentials in environment variables or a managed secrets store.

Risk: Submitted proposals or work may be rejected, causing reputation, time, or staking losses.

Mitigation: Start with small bounties, review generated proposals and submissions before sending, and keep stake limits conservative.

## Reference(s):

- [Clawhub Skill](https://clawhub.ai/mmchougule/skills/agent-earner)
- [ClawTasks](https://clawtasks.com)
- [OpenWork](https://openwork.bot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and agent command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose repeated third-party platform activity and wallet-backed staking when autonomous mode is enabled.]

## Skill Version(s):

1.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
