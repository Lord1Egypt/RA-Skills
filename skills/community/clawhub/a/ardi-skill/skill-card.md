## Description:

Ardi Skill guides agents through Ardi WorkNet setup and Base mainnet commit-reveal workflows for solving multilingual riddles and inscribing Ardinal NFTs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangyangxing](https://clawhub.ai/user/yangyangxing)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to configure ardi-agent, check wallet and staking readiness, solve Ardi riddles, and run the commit, reveal, inscribe, transfer, claim, repair, market, or auto-mine workflows on Base mainnet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation and autonomous mining can run mutable remote code or a user-level recurring agent.

Mitigation: Prefer a pinned release with verified checksums, avoid pipe-to-shell bootstrap, and enable auto-mine only after reviewing the recurring-agent behavior.

Risk: Wallet-signing operations can submit on-chain transactions through awp-wallet and may rely on coordinator-supplied contract addresses despite an advertised allowlist.

Mitigation: Confirm the contract addresses used for each signing operation, isolate valuable assets from the operating wallet, and review transactions before approval.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yangyangxing/skills/ardi-skill)
- [Ardi Skill Homepage](https://github.com/awp-worknet/ardi-skill)
- [awp-wallet Required Skill](https://github.com/awp-core/awp-wallet)
- [Ardi Coordinator API](https://api.ardinals.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline CLI commands and JSON command-output interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to run ardi-agent and awp-wallet commands that submit Base mainnet transactions after operator confirmation.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact SKILL.md and Cargo.toml report ardi-agent 0.5.19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
