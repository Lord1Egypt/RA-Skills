## Description:

Provides a Chinese-language data analysis helper for descriptive statistics, anomaly detection, trend analysis, and spreadsheet or CSV review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prompt an agent to analyze datasets, spreadsheets, CSV files, or Excel files for summary statistics, anomalies, and trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The broad Chinese trigger text may activate the skill on general data or spreadsheet requests.

Mitigation: Confirm the user wants data-analysis help and clarify the dataset, columns, and requested analysis before drawing conclusions.

Risk: Noisy reference notes may not match the user's actual analysis domain.

Mitigation: Treat the Bilibili notes as background evidence only and ground the response in the uploaded or described data.

Risk: Data-analysis outputs can be incorrect or misleading when source data is incomplete, malformed, or ambiguous.

Mitigation: Review uploaded data, state assumptions, and validate statistical conclusions before relying on the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/data-analyzer-from-bilibili)
- [Bilibili: PAZ Analyzer plugin tutorial](https://www.bilibili.com/video/BV1AikJYuEAe)
- [Bilibili: Gel-Pro analyzer 4.0 quantitative analysis software](https://www.bilibili.com/video/BV1po4y1P79E)
- [Bilibili: Aspen Energy Analyzer introduction](https://www.bilibili.com/video/BV1sR4y1K7Bv)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text analysis guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code; output depends on user-provided data and the host agent's analysis capabilities.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
