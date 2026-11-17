## Description:

Analyzes insurance-oriented Excel, CSV, or JSON datasets by running exploratory analysis, cleaning data, generating charts, preparing AI-assisted insights, and exporting Word reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwbwin](https://clawhub.ai/user/wwbwin)

### License/Terms of Use:

MIT-0

## Use Case:

Insurance analysts and business users can use this skill to inspect spreadsheet-like datasets, summarize data quality, produce common charts, and package results into a Word analysis report. It is intended for workflows where the user can review dataset-derived prompts before any external AI insight generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dataset-derived insurance information may be sent to third-party AI providers during insight generation.

Mitigation: Use a local-only workflow for customer, policy, claims, financial, health, or confidential business data, or require explicit approval after reviewing and redacting the exact prompt before any Kimi or DeepSeek call.

Risk: Generated insights and charts may be treated as final business conclusions without domain review.

Mitigation: Have an insurance or data-analysis reviewer check the generated report against the source dataset, cleaning log, and business context before acting on recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwbwin/skills/basic-data-analysis)
- [Workflow reference](references/workflow.md)
- [Insight generation reference](references/insight_generation.md)
- [Kimi chat completions endpoint](https://api.moonshot.cn/v1/chat/completions)
- [DeepSeek chat completions endpoint](https://api.deepseek.com/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [JSON summaries, PNG charts, Markdown insight text, and DOCX report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces summary.json and chart images from analyze.py, then uses reviewed insight text to generate a Word report with export_report.py.]

## Skill Version(s):

1.0.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
