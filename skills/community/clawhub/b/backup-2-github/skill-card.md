## Description:

Backs up personalized OpenClaw configuration and user data to a GitHub repository and can restore that state to a fresh OpenClaw installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangbb-coder](https://clawhub.ai/user/fangbb-coder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to migrate or recover personalized OpenClaw configuration, memory, profile, scheduled tasks, and selected custom files through a GitHub backup repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send sensitive OpenClaw memory, profile, persona, configuration, scheduled tasks, and optional credential files to GitHub.

Mitigation: Use a dedicated private repository, configure a fine-grained GitHub token, avoid command-line tokens, and review dry-run output before backing up.

Risk: Restore can overwrite persistent local OpenClaw state from repository content.

Mitigation: Restore only after verifying the repository content and commit, and keep a separate local copy of important files before proceeding.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fangbb-coder/skills/backup-2-github)
- [Publisher profile](https://clawhub.ai/user/fangbb-coder)
- [README](README.md)
- [Skill instructions](SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write backup data to GitHub and overwrite local OpenClaw state during restore when executed.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
