## Description:

Calculates illustrative net returns after management, custody, and sales fees and flags guarantee-of-principal claims in promotional text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Investors and financial-product reviewers use this skill to estimate the effect of management, custody, and sales fees on returns and to screen promotional copy for guarantee claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Illustrative returns or fees could be mistaken for an investment recommendation.

Mitigation: Check fee inputs and calculation assumptions independently; do not treat estimates as investment or legal advice.

Risk: Keyword screening can miss guarantee claims phrased differently.

Mitigation: Have a qualified reviewer check promotional language rather than treating a PASS result as compliance approval.

Risk: The skill metadata permits more tools than its inspected local workflow needs.

Mitigation: Grant only the local execution permissions needed for the calculator.

## Reference(s):

- [Fund Fee Calc on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/fund-fee-calc)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Plain text or JSON (--json)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports fee totals, illustrative gross and net returns, screening results, and an exit status.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata; bundled skill text says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
