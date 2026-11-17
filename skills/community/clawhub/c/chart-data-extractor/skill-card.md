## Description:

Extract pixel-level data from an image of a chart or graph and produce a structured data table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to extract structured values from chart images, graph screenshots, and visual tables for spreadsheet use, chart reconstruction, or further analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chart images may contain sensitive or proprietary information.

Mitigation: Only provide images that are appropriate to share with the model or approved processing environment.

Risk: Interpolated or low-confidence extracted values may be inaccurate if the chart has poor resolution, overlapping marks, unclear labels, or ambiguous scaling.

Mitigation: Review the confidence notes, assumptions, and separately flagged low-confidence values before using the extracted data in important decisions.

Risk: Misreading a logarithmic, truncated, or otherwise nonstandard axis can make extracted values misleading.

Mitigation: Confirm axis scale and chart caveats before treating the reconstructed table or CSV as authoritative.

## Reference(s):

- [Chart Data Extractor ClawHub Page](https://clawhub.ai/mohitagw15856/skills/chart-data-extractor)
- [Chart Data Extractor Homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/chart-data-extractor.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown tables, confidence notes, caveats, observations, and CSV code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flags low-confidence and interpolated values separately and includes assumptions about chart scale and readability.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
