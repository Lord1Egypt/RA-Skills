## Description:

Provides a structured code review workflow for pull request review, code quality checks, security inspection, performance analysis, and CI/CD status review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review code changes, PRs, tests, CI failures, security concerns, performance issues, and maintainability risks. It is aimed at practical feedback with prioritized findings and suggested fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect pull request and CI state through GitHub CLI.

Mitigation: Use it only where that repository access is acceptable, and review requested GitHub CLI commands before execution.

Risk: The skill includes a workflow that can commit and push CI fixes without clear final confirmation or safe staging.

Mitigation: Require the exact diff, stage only intended files, verify branch and remote, scan for secrets, and require explicit confirmation before any commit or push.

## Reference(s):

- [Code Review Reference Guide](artifact/reference.md)
- [Code Review Examples](artifact/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/skills/code-review-terry)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown review findings with optional code snippets and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prioritized issues, CI/CD status notes, concrete fix suggestions, and verification commands.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
