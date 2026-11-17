## Description:

Manage Craft notes, documents, and tasks via CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noah-ribaudo](https://clawhub.ai/user/noah-ribaudo)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to search, create, update, and manage Craft documents, daily notes, blocks, tasks, folders, and collections through CLI-oriented agent assistance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad Craft note and task access with weak scoping.

Mitigation: Use it only for explicit Craft requests and grant the narrowest Craft permissions available.

Risk: The setup guidance stores the Craft Connect URL in a shell profile, which may persist a sensitive credential-like URL in plaintext.

Mitigation: Avoid permanent shell-profile storage when possible and handle the Craft Connect URL as a sensitive secret.

Risk: The skill documents update and delete operations for blocks and tasks.

Mitigation: Require user confirmation before running any update or delete command.

Risk: The package references an install script that was not present in the inspected artifact.

Mitigation: Verify the actual CLI implementation before installing or relying on it.

## Reference(s):

- [Craft Notes on ClawHub](https://clawhub.ai/noah-ribaudo/skills/craft)
- [Publisher profile: noah-ribaudo](https://clawhub.ai/user/noah-ribaudo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Craft CLI commands and environment-variable setup; users should confirm destructive updates and deletes before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
