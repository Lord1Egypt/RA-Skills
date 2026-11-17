## Description:

Audit a multi-card wallet for overlap, gaps, and total annual cost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiahongc](https://clawhub.ai/user/jiahongc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to evaluate a set of credit cards for annual fee burden, reward-category coverage, redundant benefits, and gaps in the wallet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may provide unnecessary sensitive financial details while asking for a wallet audit.

Mitigation: Provide only card names unless a more personalized analysis is deliberately requested; do not provide banking logins, account numbers, or statements.

Risk: Credit-card fees, benefits, credits, and earning categories can change, making stale public information misleading.

Mitigation: Research current public card information, include confidence notes, and avoid treating point multipliers as statement credits.

## Reference(s):

- [Card Wallet skill page](https://clawhub.ai/jiahongc/skills/card-wallet)

## Skill Output:

**Output Type(s):** [Markdown, Analysis, Guidance]

**Output Format:** [Markdown wallet audit with annual cost, earning map, credits stack, overlap, gaps, and confidence notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses hidden YAML for sources when following the skill contract.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
