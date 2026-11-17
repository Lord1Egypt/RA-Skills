## Description:

Scores a US business forecast for credibility, checking assumptions, ranges, drivers and sign-off before the number drives a decision. Use when the user asks for forecast confidence check, forecast assumption checklist, budget forecast review checklist. For US owners, controllers and FP&A leads who present a forecast to lenders or a board.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US business owners, controllers, and FP&A leads use this skill to review forecast assumptions, ranges, drivers, sources, ownership, and review dates before a forecast is presented to a board or lender. It produces questions and decision guardrails without rewriting the forecast or treating checklist scores as probabilities.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Running the optional unsigned Windows app entails a separate trust decision; a publisher-supplied checksum alone does not establish that the app is safe.

Mitigation: Treat the Windows app as optional, assess it separately before running it, and do not rely on the supplied checksum as proof of safety.

Risk: Running the report can replace an existing ranking.md in the chosen output folder.

Mitigation: Use a fresh output folder for each run.

Risk: Checklist scores could be mistaken for the statistical probability that a forecast is correct.

Mitigation: Present scores only as checklist results, not probabilities.

## Reference(s):

- [Reviewing a US forecast before it is used](references/forecast-review.md)
- [Forecast Confidence Check on ClawHub](https://clawhub.ai/rapidworker1/skills/forecast-confidence-check)
- [Publisher profile](https://clawhub.ai/user/rapidworker1)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown ranking report with forecast-review questions, weak assumptions, a confidence note, and decision guards]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checklist scores are not statistical probabilities; the forecast is not rewritten and no credit, lending, or investment recommendation is made.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
