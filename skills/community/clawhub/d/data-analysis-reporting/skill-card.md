## Description: <br>
Turns raw business data from CSV, SQLite, spreadsheets, and pasted tables into clear analytical summaries, trend analysis, and actionable reports with plain-language insights and explicit confidence labels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gitcanadabrett](https://clawhub.ai/user/gitcanadabrett) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Small business operators, analysts, founders, consultants, and decision-makers use this skill to turn provided business datasets into readable reports, quality notes, trend findings, comparisons, and recommended next steps. It is intended for analytical support, not financial, investment, tax, or audit-grade advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may paste real PII, secrets, or sensitive production data into the chat while requesting analysis. <br>
Mitigation: Remove or redact sensitive fields before sharing data, and use the skill's PII detection and exclusion workflow before any analysis. <br>
Risk: A test prompt contains unmasked SSN-style mock values. <br>
Mitigation: Treat those examples as unsafe placeholders; the publisher should replace them with clearly synthetic or redacted values. <br>
Risk: Business analysis output could be mistaken for financial advice, firm forecasts, or audit-grade reporting. <br>
Mitigation: Use the reports as analytical aids only, keep forecasts labeled with assumptions and confidence, and avoid investment, tax, or audit conclusions. <br>
Risk: Release metadata includes unrelated crypto and purchase capability tags. <br>
Mitigation: Do not rely on those tags to determine this skill's behavior; the publisher should remove or correct unrelated capability metadata. <br>


## Reference(s): <br>
- [Data Analysis Reporting Spec](data-analysis-reporting-spec.md) <br>
- [Business Metrics Reference](references/business-metrics.md) <br>
- [Data Quality Checks](references/data-quality-checks.md) <br>
- [Report Templates](references/report-templates.md) <br>
- [Test Prompts](references/test-prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown analytical reports with executive summaries, data quality notes, key findings, trend analysis, comparisons, recommended actions, and methodology notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes confidence labels and data-quality caveats; excludes detected PII from analysis.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
