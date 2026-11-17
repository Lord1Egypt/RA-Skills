## Description:

Access passwords, secure notes, secrets and OTP codes from Dashlane vault.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gnarco](https://clawhub.ai/user/gnarco)

### License/Terms of Use:


## Use Case:

Developers and employees use this skill to guide an agent in retrieving Dashlane vault items, OTP codes, secure notes, secrets, and related CLI configuration through Dashlane CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-invoked Dashlane CLI commands can reveal vault contents, including passwords, secure notes, secrets, and OTP codes.

Mitigation: Use only in trusted environments, review commands before execution, and limit access to the specific vault items required for the task.

Risk: Console, JSON, or broad query outputs can expose secrets in logs, transcripts, shell history, or downstream tools.

Mitigation: Prefer narrow filters and clipboard output when practical, avoid broad JSON dumps, and clean up any logs or files that may contain secret values.

Risk: Inline master-password environment variables, local backups, and disabled user-presence checks can weaken vault protections.

Mitigation: Use isolated automation setups with strong cleanup, avoid current-directory backups, and keep user-presence or keychain protections enabled unless there is a deliberate operational requirement.

## Reference(s):

- [Dashlane CLI documentation](https://cli.dashlane.com)
- [ClawHub Dashlane skill release](https://clawhub.ai/gnarco/skills/dashlane)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may reference dcli clipboard, console, and JSON outputs; vault secret values should be handled as sensitive data.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
