## Description:

CI/CD Watchdog helps DevOps teams parse failed pipeline logs, identify likely root causes, and generate Markdown repair, rollback, and post-mortem guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boboy-j](https://clawhub.ai/user/boboy-j)

### License/Terms of Use:

MIT-0

## Use Case:

DevOps engineers and development teams use this skill to troubleshoot failed CI/CD jobs by supplying relevant log excerpts and repository context. The skill produces diagnostics, suggested fixes, rollback guidance, and prevention checklists for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pipeline logs may contain tokens, passwords, internal IPs, or other sensitive operational details.

Mitigation: Provide only the relevant failure excerpt and redact secrets before using the skill.

Risk: Suggested repair, verification, or rollback commands may be incorrect or unsafe for a production environment.

Mitigation: Review all proposed commands, run dry-runs where possible, and follow change approval before execution.

Risk: The workflow is primarily Chinese-language, which may create review gaps for teams that cannot evaluate Chinese diagnostics.

Mitigation: Confirm reviewers are comfortable with the language or translate the output before relying on it for operational decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/boboy-j/skills/ci-cd-watchdog)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown diagnostic report with tables, command snippets, rollback guidance, post-mortem draft, and checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a pipeline log excerpt; optional CI platform and repository context improve specificity.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
