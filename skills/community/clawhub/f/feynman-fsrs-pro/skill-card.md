## Description:

Feynman FSRS Pro is a Feynman-style study tutor that coordinates Obsidian notes with a PostgreSQL memory store to guide spaced-repetition review using an FSRS-inspired workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sheldon-mmmp](https://clawhub.ai/user/sheldon-mmmp)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and developers use this skill to run structured Feynman-method review sessions over an Obsidian vault, including note synchronization, due-card review, targeted questioning, follow-up prompts, and progress recording.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to a local Obsidian vault and a PostgreSQL database that may contain study history and note metadata.

Mitigation: Install only in an environment where this local data access is acceptable, and limit vault and database permissions to the notes and tables needed for study review.

Risk: The artifact includes hardcoded PostgreSQL credentials.

Mitigation: Move credentials into protected configuration before use and rotate the exposed password.

Risk: The database initialization script drops and recreates the feynman_memory table.

Mitigation: Back up any existing database before running the schema and review destructive SQL statements before execution.

Risk: The artifact invokes Obsidian CLI commands through shell strings.

Mitigation: Change command execution to argument-array execution and validate note paths before running the helper scripts.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/sheldon-mmmp/skills/feynman-fsrs-pro)
- [Publisher profile](https://clawhub.ai/user/sheldon-mmmp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown conversation with structured review status, prompts, feedback, summaries, and command-oriented database or note operations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires access to a local Obsidian vault and PostgreSQL-backed study memory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
