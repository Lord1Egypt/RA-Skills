## Description:

Caveman Commit helps an agent produce terse Conventional Commit messages that preserve intent and reasoning while avoiding noisy narration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanford](https://clawhub.ai/user/seanford)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to turn staged changes or commit-message requests into concise, ready-to-paste Conventional Commit messages. It emphasizes why a change matters, while adding a body only for breaking changes, migrations, security fixes, reversions, linked issues, or non-obvious reasoning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Staged diffs may contain sensitive content that could be summarized into chat while generating a commit message.

Mitigation: Use only in repositories where staged changes are appropriate to expose to the agent, and review the generated commit message before use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown code block containing a Conventional Commits message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not run git commands, stage files, amend commits, or write files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
