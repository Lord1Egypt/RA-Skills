## Description:

Generates Conventional Commits-style Git commit messages from change descriptions or diffs, including type, scope, subject, body, and issue references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gnllk](https://clawhub.ai/user/gnllk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill after code changes to draft clear, structured Git commit messages that follow Conventional Commits and can reference issues or requirement numbers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce commit messages that omit or misstate parts of the actual change.

Mitigation: Review and edit the generated message against the diff before committing.

Risk: Keyword activation may be unexpected in mixed Chinese and English development conversations.

Mitigation: Invoke the skill with explicit commit-message requests when that assistance is intended.

Risk: Optional package commands in reference material can change behavior if dependencies are not pinned.

Mitigation: Use pinned versions or lockfile-backed project scripts before following optional npx examples.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gnllk/skills/commit-message-generator)
- [Conventional Commits reference](references/conventional-commits.md)
- [Commit message examples](references/commit-examples.md)
- [Conventional Commits](https://www.conventionalcommits.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with a generated commit message in a fenced code block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language output; generated commit messages should be reviewed before use.]

## Skill Version(s):

1.0.0 (source: evidence release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
