## Description:

Generates Chinese structured corporate innovation and credit-analysis briefs from patent, paper, and public web evidence for bank credit review workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Bank relationship managers, credit reviewers, and risk-control teams use this skill to evaluate a company's innovation capacity and generate a structured brief for credit decision support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional HTML export may turn report content or company names into active code or unintended file writes.

Mitigation: Review generated reports before opening exports, avoid attacker-supplied company names or report content, and update the exporter to use data-only inputs, sanitized filenames, contained output paths, and safe HTML rendering.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/corp-innovation-brief)
- [PatSnap open platform](https://open.zhihuiya.com/)

## Skill Output:

**Output Type(s):** [Markdown, Files, Code, Configuration guidance]

**Output Format:** [Chinese Markdown report with optional self-contained HTML export and JSON data structure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured PatSnap and public web data access; HTML export should occur only after user confirmation.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
