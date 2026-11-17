## Description:

FeedbackLens Analysis clusters user feedback from text, CSV, or Excel files, scores priorities with a frequency, severity, and impact-scope algorithm, generates actionable improvement suggestions, and renders visual reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongtotti](https://clawhub.ai/user/dongtotti)

### License/Terms of Use:

MIT-0

## Use Case:

External users, product teams, support teams, and developers use this skill to analyze batches of user feedback, prioritize issue clusters, and produce report-ready recommendations. It supports real feedback analysis and a built-in demo mode for seeing the workflow without preparing data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads feedback files selected for analysis and writes report files in the workspace.

Mitigation: Run it only on intended feedback files and review the workspace outputs before distributing them.

Risk: Generated reports may include original feedback quotes.

Mitigation: Review, redact, or remove sensitive user feedback before sharing reports outside the intended audience.

Risk: Generated reports include a visible FeedbackLens footer link with UTM parameters.

Mitigation: Confirm that the footer link is acceptable for the deployment context before publishing or sharing the report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dongtotti/skills/feedbacklens-analysis)
- [FeedbackLens web app](https://www.feedbacklens.cn/?utm_source=workbuddy_skill&utm_medium=report_footer&utm_campaign=feedbacklens_analysis&utm_content={demo|real_report})
- [Artifact README](artifact/README.md)
- [Industry severity anchors](artifact/priority_cases.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance, files]

**Output Format:** [Text or Markdown summaries, JSON evaluation records, and HTML report files with optional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write report artifacts under evaluations/ and may include original feedback quotes in generated reports.]

## Skill Version(s):

1.2.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
