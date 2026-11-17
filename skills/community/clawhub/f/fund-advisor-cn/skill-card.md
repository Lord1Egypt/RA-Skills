## Description:

Fund Advisor Cn helps agents provide fund screening, dollar-cost averaging strategy, asset allocation, risk assessment, return calculations, and portfolio rebalancing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to calculate fund investment scenarios, compare expected returns, plan asset allocation, evaluate risk metrics, and produce rebalancing suggestions. Its outputs are generic calculations and educational guidance rather than licensed financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce actionable fund allocation, rebalancing, Kelly, and return guidance that may be unsuitable for a user's financial circumstances.

Mitigation: Treat outputs as educational calculations, review recommendations with a qualified financial adviser, and avoid relying on them as licensed financial advice.

Risk: Some financial tracking commands may persist transaction descriptions or command history in local plaintext files.

Mitigation: Avoid entering sensitive transaction details unless local plaintext storage is acceptable, and inspect or delete the fund-advisor-cn data directory when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/fund-advisor-cn)
- [Fund investment guide](artifact/tips.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and plain text with command examples and calculator-style summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces generic financial calculations and guidance; some companion commands may write local plaintext history under the fund-advisor-cn data directory.]

## Skill Version(s):

2.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
