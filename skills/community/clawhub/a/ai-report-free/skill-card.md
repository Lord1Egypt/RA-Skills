## Description:

AI财报分析 helps agents analyze financial report content, produce F-score summaries, flag risk warnings, and return structured finance-analysis results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External finance users, analysts, and agent builders use this skill to process financial report data, summarize F-score-style signals, flag risk warnings, and generate structured analysis for investment, credit-risk, or forecasting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad command execution for finance-analysis workflows.

Mitigation: Review the skill before installation, run it only in a trusted agent workspace, and prefer a release that documents exact commands, consent prompts, and local-only behavior.

Risk: Financial reports, API keys, or other sensitive inputs may be exposed to external data or API services.

Mitigation: Avoid providing sensitive financial reports or API keys unless the receiving services are understood and approved; use least-privileged, rotated credentials.

Risk: Generated financial scores, forecasts, and risk warnings can be incomplete or misleading.

Mitigation: Require human review before using outputs for investment, credit-risk, compliance, or other material financial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ai-report-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)
- [Skill homepage](https://skillhub.cn)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples, Python snippets, and optional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference external financial data or API services and may require API keys depending on the data source.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
