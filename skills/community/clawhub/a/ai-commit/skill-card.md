## Description:

Analyze staged changes and generate semantic commit messages automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afine907](https://clawhub.ai/user/afine907)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect staged Git changes, propose conventional commit messages, and optionally create or amend commits from reviewed staged changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create a real Git commit or amend the latest commit.

Mitigation: Review staged changes with git diff --staged and use /commit --dry-run when only a proposed message is desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/afine907/skills/ai-commit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and conventional commit message text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or amend Git commits when the user chooses an executing command rather than a dry run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
