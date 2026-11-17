## Description:

Automated code review, quality gates, and PR analysis. Integrates with GitHub, GitLab, Bitbucket. Enforce style guides, detect bugs, security vulnerabilities, performance issues. Auto-approve safe PRs, flag dangerous changes. Save developers 5+ hours/week on manual reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuczy](https://clawhub.ai/user/fuczy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to automate pull request review, enforce coding standards, detect likely bugs and security issues, and produce review comments or merge-blocking guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent repository access and automated PR approvals can bypass intended human or code-owner review.

Mitigation: Limit installation to selected repositories, prevent bot approvals from satisfying required human reviews, and disable or tightly restrict auto-approve.

Risk: Private repository or pull request data may be sent to ClawHub or notification integrations.

Mitigation: Confirm data handling before using the skill on private or sensitive codebases and scope repository permissions to the minimum needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fuczy/skills/clawd-code-reviewer)
- [Publisher Profile](https://clawhub.ai/user/fuczy)
- [Skill Homepage](https://clawhub.com/skills/code-reviewer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown review comments, YAML configuration, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May interact with repository and pull request data through configured Git hosting tools.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
