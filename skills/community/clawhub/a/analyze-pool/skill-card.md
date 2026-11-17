## Description:

Analyze a specific Uniswap pool's performance, liquidity depth, fee APY, and risk factors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers, analysts, and DeFi users use this skill to evaluate a specific Uniswap pool before LPing or trading heavy size. It summarizes pool identification, TVL, price, historical volume, fee APY, liquidity depth, concentration, and risk factors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable install commands can change what is installed over time.

Mitigation: Prefer a reviewed ClawHub release or pin the installer and source reference before installing.

Risk: The skill delegates work to a pool-researcher subagent and uses the opus model, which may affect model access, cost, and review requirements.

Mitigation: Confirm the subagent configuration and model choice are acceptable for the target environment before deployment.

Risk: Pool metrics and fee APY can be misread as financial advice or guaranteed future performance.

Mitigation: Present fee APY as historical, keep wallet/private-key workflows out of scope, and require users to make independent financial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/analyze-pool)
- [Artifact skill specification](artifact/SKILL.md)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, analysis, guidance]

**Output Format:** [Markdown summary with pool metrics, liquidity depth, performance figures, and risk notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Delegates pool research to a configured pool-researcher subagent and reports missing pools, unrecognized tokens, or limited data clearly.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
