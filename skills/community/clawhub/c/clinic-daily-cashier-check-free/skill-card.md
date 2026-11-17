## Description:

Checks clinic outpatient cashier and refund daily reconciliation tables for arithmetic consistency, totals, duplicate rows, blanks, and negative amounts, with source-cited findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Hospital and clinic cashiers or cashier supervisors use this skill before daily close to check outpatient payment and refund reconciliation tables. It helps verify row arithmetic, column totals, duplicate entries, blank placeholders, and negative amounts without making medical, pricing, insurance, or responsibility judgments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes clinic reconciliation data through a local Node.js script.

Mitigation: Run it only in environments approved for that data and review inputs and outputs before operational use.

Risk: The free release performs only the listed free subset of checks.

Mitigation: Treat results as a limited reconciliation aid and separately review excluded financial, insurance, medical, and policy questions.

Risk: The interface and output are primarily Chinese.

Mitigation: Use it with reviewers who can reliably understand and validate Chinese-language reconciliation output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/clinic-daily-cashier-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Human-readable text or structured JSON containing executed checks, omitted checks, notes, missing-input guidance, and source-cited reconciliation findings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js and reports insufficient input without producing a reconciliation conclusion.]

## Skill Version(s):

1.0.52 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
