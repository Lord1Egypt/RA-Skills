## Description:

Triggers on any task that modifies code. Provides instructions to surgically stage and commit only the modified code files to save progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shangter666](https://clawhub.ai/user/shangter666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to save completed code changes by staging only explicitly modified source or documentation files and creating a concise git commit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause agents to create git commits automatically, which may persist partial, experimental, or sensitive changes in repository history.

Mitigation: Use it only in repositories where automatic commits are desired, explicitly opt out for sensitive or unfinished work, and review staged files and recent history after the agent runs.

Risk: Sensitive files or generated artifacts could be committed if file selection is not reviewed carefully.

Mitigation: Follow the skill's surgical staging and ignore-list guidance, verify `git status` before committing, and keep credentials, binaries, and build outputs out of staged changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shangter666/skills/auto-commit)
- [Auto-Commit Ignore List](references/ignore_list.txt)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may result in persistent repository history changes when followed.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
