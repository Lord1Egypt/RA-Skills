## Description:

An AI-assisted international news reporting toolkit that helps agents create daily reports using structured workflows, source verification, Markdown templates, and PDF generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ywwzzsgit](https://clawhub.ai/user/ywwzzsgit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and AI agents use this skill to prepare international daily news briefings from current public sources, organize evidence by source reliability, draft Markdown analysis, and optionally generate a PDF report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: News reports can contain incomplete, stale, or misleading information from public search results.

Mitigation: Treat generated reports as drafts and verify critical claims against multiple high-reliability sources before relying on them.

Risk: Sensitive private context could be exposed through external news-search queries.

Mitigation: Avoid including private, confidential, or personal data in search prompts or report inputs.

Risk: The bundled PDF utility may generate sample-style Chinese report content rather than faithfully converting the provided Markdown input.

Mitigation: Review generated PDFs against the source Markdown before distributing or using them for decisions.

## Reference(s):

- [Source Directory](references/source_directory.md)
- [Daily Report Template](assets/templates/daily_report_template.md)
- [ClawHub Skill Page](https://clawhub.ai/ywwzzsgit/skills/daily-news-reporter)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown report content with optional PDF output and source-attributed analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AI agent with web search capability for data collection; PDF generation uses the bundled Python utility.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
