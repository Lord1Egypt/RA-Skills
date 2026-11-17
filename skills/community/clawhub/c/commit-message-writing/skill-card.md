## Description:

Strict Conventional Commits v1.0.0, atomic commit discipline, and Trunk-Based Development guardrails for git work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omaression](https://clawhub.ai/user/omaression)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when preparing commits, reviewing staged changes, writing Conventional Commit messages, splitting mixed work into atomic commits, and validating messages before commit or pull request review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included Git commit-msg hook can run validator code from repository-controlled relative paths and skips validation if no validator is found.

Mitigation: Review the hook before installation; use a trusted fixed validator path and make the hook fail closed when validation cannot run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/omaression/skills/commit-message-writing)
- [Publisher profile](https://clawhub.ai/user/omaression)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline bash commands and validator output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes guidance for commit structure, branch posture, change splitting, PR test expectations, and local commit-message validation.]

## Skill Version(s):

1.0.0-alpha (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
