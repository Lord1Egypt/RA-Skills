## Description:

Chain Sensei provides on-chain intelligence for AI agents by analyzing wallets, detecting risks, tracing transactions, and returning insights for Ethereum addresses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agustinastie2](https://clawhub.ai/user/agustinastie2)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and AI-agent operators use this skill to request wallet snapshots, token information, transaction traces, risk scoring, batch analysis, and event alerts across supported EVM chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Premium x402 features and alerts can cause paid requests or recurring paid triggers.

Mitigation: Enable x402 only with explicit spending limits, per-request approval, and a way to disable alerts or recurring triggers.

Risk: The install command uses an unpinned remote installer, so installation behavior can change over time.

Mitigation: Use a pinned, trusted installer version where possible and review the skill before installing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agustinastie2/skills/chain-sensei)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Natural-language summaries and structured JSON for wallet, token, transaction, and risk-analysis results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use a local file cache; premium features can involve x402 payments when enabled.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
