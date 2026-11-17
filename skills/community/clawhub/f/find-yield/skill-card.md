## Description:

Find the highest-yield LP pools on Uniswap filtered by risk tolerance and minimum TVL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers, DeFi analysts, and liquidity providers use this skill to compare Uniswap LP pools by yield, risk tolerance, chain, capital amount, and minimum TVL before deciding which opportunities to investigate further.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Yield rankings may be mistaken for guaranteed returns or financial advice.

Mitigation: Present results as informational, note that APY is historical, and remind users that past performance does not guarantee future returns.

Risk: Delegated pool scans depend on the separate opportunity-scanner agent.

Mitigation: Review and trust the opportunity-scanner agent before relying on delegated scan results.

Risk: LP opportunities can expose users to impermanent loss and volatile-pair risk.

Mitigation: Surface risk tolerance, TVL filters, and impermanent-loss considerations alongside ranked yield results.

Risk: Mutable install commands can change over time.

Mitigation: Install from a trusted or pinned source when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/find-yield)
- [README](artifact/README.md)
- [Skill specification](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown table with concise explanatory notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ranked Uniswap LP yield opportunities with APY, TVL, chain, risk, and user-facing error messages when no matching pools are found or chain scans are incomplete.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
