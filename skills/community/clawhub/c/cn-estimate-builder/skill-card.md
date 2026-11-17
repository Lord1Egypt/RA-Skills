## Description:

Builds construction project estimates with category-level cost breakdowns, markups, validation warnings, and tabular reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruiyongwang](https://clawhub.ai/user/ruiyongwang)

### License/Terms of Use:

MIT-0

## Use Case:

Construction estimators, project managers, and cost engineers use this skill to assemble line-item construction estimates, apply markups, summarize costs by category, and flag basic estimate issues before review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Construction estimates, standards, rates, currencies, and category mappings may be incorrect or incomplete for bids, contracts, or regulatory submissions.

Mitigation: Treat outputs as draft calculations and verify applicable standards, rates, currency, category mappings, and project assumptions with qualified reviewers before use.

Risk: Spreadsheet export paths can write files to user-selected locations.

Mitigation: Use deliberate, trusted export paths and inspect generated workbooks before sharing or relying on them.

Risk: The release has reliability and scope-documentation issues according to the security summary.

Mitigation: Use the skill within its construction-estimating scope and reconcile results with local estimate formats and project requirements.

## Reference(s):

- [DataDrivenConstruction homepage](https://datadrivenconstruction.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown tables and narrative guidance with optional Python code examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include category totals, markup breakdowns, grand totals, and validation warnings rounded to two decimal places.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
