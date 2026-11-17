## Description:

Help address review/issue comments on the open GitHub PR for the current branch using gh CLI; verify gh auth first and prompt the user to authenticate if not logged in.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tbeard602](https://clawhub.ai/user/tbeard602)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect GitHub pull request review comments on the current branch, summarize actionable threads, and apply user-selected fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses GitHub PR discussion data and the user's gh authentication.

Mitigation: Use a fine-grained, least-privilege GitHub token scoped to the target repository.

Risk: The skill requests broader GitHub privileges and elevated command execution than its helper code needs.

Mitigation: Avoid granting workflow scope unless a specific user-approved change requires it, and review commands before running them with elevated permissions.

Risk: The skill can apply repository changes based on selected PR comments.

Mitigation: Review proposed file or repository changes before they are applied.

## Reference(s):

- [GitHub Address Comments on ClawHub](https://clawhub.ai/tbeard602/skills/gh-address-comments)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and code changes when the user selects comments to address]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read GitHub PR comments through gh CLI and propose or apply repository changes after user selection.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
