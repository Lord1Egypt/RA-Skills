## Description:

Provides systematic code review guidance for pull requests and code changes, including code quality, security, performance, maintainability, tests, and CI/CD status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review pull requests or local code changes, check CI/CD failures, and produce prioritized review feedback with concrete remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to modify, commit, and push repository changes while handling CI failures.

Mitigation: Use read-only review by default, request fixes explicitly, and review the exact staged diff and target branch before any commit or push.

Risk: The skill uses GitHub CLI and existing Git credentials to inspect pull requests, checks, and workflow logs.

Mitigation: Run it only in repositories and GitHub sessions where the agent should have review access, and avoid granting broader repository permissions than needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/ai-code-review-ops)
- [Code Review Reference Guide](artifact/reference.md)
- [Code Review Examples](artifact/examples.md)
- [The Twelve-Factor App: Config](https://12factor.net/config)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown review comments with optional code and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prioritized findings, CI/CD status summaries, remediation steps, and local verification commands.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
