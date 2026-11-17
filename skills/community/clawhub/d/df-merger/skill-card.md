## Description:

Merge pandas DataFrames from multiple construction sources. Handle different schemas, keys, and data quality issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

Developers and construction data practitioners use this skill to merge BIM, schedule, cost, quantity takeoff, sensor, or other project DataFrames while reconciling schema differences and assessing merge quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The activation wording is broader than necessary and may cause unrelated construction project-management materials to be processed.

Mitigation: Use the skill for explicit DataFrame merging or cleanup tasks and provide only the relevant user-supplied datasets.

Risk: Automatic schema harmonization and fuzzy matching can create incorrect joins when columns, IDs, or descriptions are ambiguous.

Mitigation: Validate merge keys, inspect match scores and unmatched row counts, and review merged samples before using results for project decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/datadrivenconstruction/skills/df-merger)
- [Data Driven Construction](https://datadrivenconstruction.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with Python code examples and structured table-oriented results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include merge quality statistics, matched and unmatched row counts, key findings, and suggested export formats such as Excel, CSV, or JSON.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
