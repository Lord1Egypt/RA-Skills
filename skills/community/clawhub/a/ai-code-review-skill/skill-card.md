## Description:

Helps agents review pull requests and code changes for code quality, security, tests, performance, maintainability, and CI status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to guide agent-assisted pull request and code review, including CI status checks and prioritized feedback on quality, security, tests, performance, and maintainability. When reviewing the agent's own PR, the skill may also guide CI failure diagnosis and repair.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to repair CI failures on its own PR and then commit and push changes, including broad staging.

Mitigation: Require approval before edits, stage explicit files only, show git status and staged diff, check for secrets, and confirm the remote and branch before any push.

Risk: Review feedback and suggested fixes may be incomplete or incorrect for the target codebase.

Mitigation: Treat recommendations as review assistance and require a human reviewer to verify findings, code changes, and CI interpretations before merge or deployment.

## Reference(s):

- [Detailed Review Criteria](artifact/reference.md)
- [Review Examples](artifact/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/skills/ai-code-review-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown review feedback with inline shell commands and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on Git and GitHub CLI context when reviewing pull requests or CI failures.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
