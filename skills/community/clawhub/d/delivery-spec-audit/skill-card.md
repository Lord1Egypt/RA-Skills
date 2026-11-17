## Description:

Audits a completed coding task by extracting change and verification evidence from session logs, then comparing it with the requirements to identify coverage gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z-zihan](https://clawhub.ai/user/z-zihan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use the skill when a coding task is nearing completion to compare stated requirements with recorded changes and verification evidence. It produces a coverage matrix that distinguishes supported findings from suspected gaps and insufficient evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan is benign with medium confidence; unresolved local references and a low-probability credential-access flag leave some uncertainty.

Mitigation: Review the unresolved references and flagged behavior before installation; do not rely on the benign verdict alone.

Risk: Session logs and extracted file paths may contain sensitive project details.

Mitigation: Use trusted local session logs and review extracted evidence before sharing the audit report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/z-zihan/skills/delivery-spec-audit)
- [Project homepage (skill metadata)](https://github.com/z-Zihan/awesome-skills)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON]

**Output Format:** [Markdown audit report with a coverage matrix; optional JSON evidence summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates command counts from pass/fail results and labels evidence limitations.]

## Skill Version(s):

1.2.1 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
