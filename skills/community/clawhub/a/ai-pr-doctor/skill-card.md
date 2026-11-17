## Description:

AI PR Doctor automates GitHub pull request diagnosis, multi-dimensional AI code review, bug repair, repair reporting, and optional merging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, maintainers, and DevOps teams use this skill to review GitHub pull requests, attempt simple fixes, rerun tests, optionally merge approved changes, and publish a repair report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make high-impact repository changes, including automated fixes and optional pull request merging.

Mitigation: Use it only on repositories where autonomous PR modification is acceptable, disable auto_merge by default, restrict GitHub token permissions, and require human approval before merging when review failures or security-sensitive changes are present.

Risk: The skill can publish repair reports to Feishu, which may expose PR details outside the repository workflow.

Mitigation: Disable notify_feishu by default unless external reporting is approved, verify destination permissions, and review report contents for sensitive information before publication.

Risk: User-configurable test commands can run shell commands during the repair workflow.

Mitigation: Allow only trusted test_command values from maintainers and avoid running untrusted commands from pull request authors.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Structured review results and Markdown repair reports with command and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce PR status, issue counts, fixed-file counts, merge state, and Feishu document identifiers when reporting is enabled.]

## Skill Version(s):

1.0.0 (source: workflow.json and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
