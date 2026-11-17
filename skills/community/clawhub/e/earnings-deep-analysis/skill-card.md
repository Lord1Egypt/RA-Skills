## Description:

Earnings Deep Analysis helps agents produce Chinese-language deep-dive earnings reports that analyze financial statements, earnings quality, revenue, margins, expenses, profitability, cash flow, working capital, anomalies, risks, and investment implications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xinxindefeiyu](https://clawhub.ai/user/xinxindefeiyu)

### License/Terms of Use:

Custom Baidu internal-use license

## Use Case:

External analysts, financial-content teams, and agents use this skill to turn company financial reports, research notes, operating data, or company-period inputs into a structured Chinese-language earnings analysis. It is intended for full earnings reviews, anomaly checks, and report generation rather than single data-point lookup, trading recommendations, chart reading, or personal trade review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated analysis may combine user-provided financial documents with web-searched public data and influence investment discussions.

Mitigation: Review the generated HTML report and extracted JSON before sharing, verify cited data sources, and treat investment implications as analytical context rather than buy or sell advice.

Risk: Missing, conflicting, or weak source material can lead to unsupported financial conclusions.

Mitigation: Keep absent values marked as unavailable, preserve conflicts for confirmation, and require company and reporting-period clarity before completing the report.

Risk: A report may appear complete while still containing placeholders, omitted required sections, or inadequate anomaly coverage.

Mitigation: Run the bundled earnings lint gate and fix blocking failures before delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xinxindefeiyu/skills/earnings-deep-analysis)
- [Financial analysis framework](references/analysis-framework.md)
- [Operating anomaly checklist](references/anomaly-checklist.md)
- [HTML report output template](references/output-template.md)
- [Generated output README](outputs/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Chinese-language analysis with self-contained HTML report files, extracted-data JSON files, and QA command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are expected to include 13 required sections, tag data sources, separate facts from judgment, avoid buy/sell recommendations, and pass the bundled earnings lint gate before delivery.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
