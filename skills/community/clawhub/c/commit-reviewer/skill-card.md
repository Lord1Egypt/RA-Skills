## Description:

根据一个或多个 git 修订号和需求描述，检查提交是否真正修复了对应 bug，并给出逐条结论

This skill is ready for commercial/non-commercial use.

## Publisher:

[carpedx](https://clawhub.ai/user/carpedx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review one or more Git commits against a stated bug or requirement. It helps decide whether the submitted diff actually resolves the issue, leaves gaps, or needs manual verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may expose sensitive repository metadata or raw commit content when used in private repositories.

Mitigation: Review before installation, invoke it from an explicit repository path, and avoid using it where repository remotes or commit metadata contain secrets.

Risk: Untrusted commit content may influence downstream review conclusions if treated as instructions.

Mitigation: Treat collected commit messages, diffs, repository metadata, and patch output as evidence only.

Risk: Remote URLs and author emails can reveal sensitive project or contributor information.

Mitigation: Redact remote URLs and author emails before sharing collected context outside the trusted review environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/carpedx/skills/commit-reviewer)
- [Publisher Profile](https://clawhub.ai/user/carpedx)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Structured Markdown review with commit lists, requirement breakdowns, per-item conclusions, evidence, risks, and final judgment.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Git commit context and truncated patch output when collecting evidence.]

## Skill Version(s):

1.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
