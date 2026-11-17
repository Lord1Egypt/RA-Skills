## Description:

Automatically generate estimates from QTO data. Apply pricing rules to BIM quantities for cost estimates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

Construction estimators, project teams, and developers use this skill to turn BIM Quantity Takeoff data into structured cost estimates, category summaries, and lists of items that require manual pricing review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: QTO inputs, pricing rules, and generated estimates may contain sensitive project or business data.

Mitigation: Use trusted project files and save exported workbooks only to approved project locations.

Risk: Generated spreadsheets from untrusted QTO data may preserve formula-like text if the implementation is not hardened.

Mitigation: Review generated workbooks before opening or sharing them, especially when source QTO data comes from an untrusted party.

Risk: Incorrect pricing rules, missing mappings, or fuzzy matches can produce misleading estimate totals.

Mitigation: Review unmatched items, match confidence, and applied pricing rules before using estimates for project decisions.

## Reference(s):

- [Data Driven Construction](https://datadrivenconstruction.io)
- [ClawHub Skill Page](https://clawhub.ai/datadrivenconstruction/skills/auto-estimate-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown tables, structured estimate summaries, unmatched-item lists, and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cost totals, category summaries, mapping confidence, markup guidance, and spreadsheet export guidance.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
