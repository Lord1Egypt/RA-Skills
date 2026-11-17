## Description:

CR Automated guides agents through code review, CI status checks, security review, performance analysis, and structured feedback for pull requests or local changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review pull requests or changed code, check CI status, identify code quality, security, performance, testing, and maintainability issues, and produce prioritized review feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may direct an agent to commit or push repository changes while repairing CI failures.

Mitigation: Require explicit approval before edits, review git status and staged diffs, avoid broad git add commands, and run or approve push commands only after confirming the target branch and remote.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/cr-automated)
- [Code Review Reference Guide](artifact/reference.md)
- [Code Review Examples](artifact/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with review findings, suggested code changes, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CI status summaries and recommended remediation steps.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
