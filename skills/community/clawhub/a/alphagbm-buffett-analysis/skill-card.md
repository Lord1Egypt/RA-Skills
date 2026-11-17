## Description:

Alphagbm Buffett Analysis produces a Warren Buffett-style scorecard for a US stock ticker, scoring business simplicity, moat, management, and valuation before returning an overall HOLDABLE, WATCHABLE, or AVOID verdict.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to request a Buffett-style assessment of a US stock ticker and receive a structured scorecard with reasoning across business, moat, management, valuation, and overall verdict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can return opinionated investment labels such as HOLDABLE, WATCHABLE, or AVOID.

Mitigation: Treat the output as research analysis rather than trading advice and review the scorecard reasoning before making investment decisions.

Risk: Invoking the skill may spend one stock-analysis credit for an uncached ticker request.

Mitigation: Use explicit Buffett-related prompts and confirm the intended ticker before invocation.

## Reference(s):

- [AlphaGBM](https://alphagbm.com)
- [ClawHub skill page](https://clawhub.ai/clementgu/skills/alphagbm-buffett-analysis)

## Skill Output:

**Output Type(s):** [analysis, markdown, guidance]

**Output Format:** [Markdown with structured scorecard fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Consumes one stock-analysis credit per uncached ticker request; cached ticker results are described as free for 30 minutes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
