## Description:

Reviews earnings quality before valuation from user-supplied structured financial statements and optional notes, without direct data fetching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teahann](https://clawhub.ai/user/teahann)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and valuation analysts use this skill to review whether reported earnings are cash-backed and reliable enough to support valuation confidence. It summarizes input quality, cash conversion, accrual risk, working-capital pressure, leverage/refinancing risk, one-off adjustments, red flags, confidence impact, and data gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive or confidential financial statements may be processed if the skill is invoked in a valuation workflow.

Mitigation: Use only financial data that the user is permitted to process in the target agent environment, and avoid submitting confidential statements unless that environment is approved for them.

Risk: The review can be lower-confidence when notes, cash-flow data, or other key line items are missing.

Mitigation: Apply the skill's data quality gate, disclose gaps in the handoff bundle, and cap confidence when relevant notes are missing or material red flags remain unresolved.

Risk: Earnings-quality findings could be mistaken for trading advice.

Mitigation: Treat red flags as valuation-risk inputs and preserve the skill's guardrail against absolute buy or sell instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teahann/skills/earnings-quality-reviewer)
- [Publisher profile](https://clawhub.ai/user/teahann)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with fixed sections and a structured handoff bundle]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses only supplied financial statements and optional notes; confidence is capped when relevant notes are missing or red flags are unresolved.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
