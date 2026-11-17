## Description:

Set up and use Bitwarden CLI (bw). Use when installing the CLI, authenticating (login/unlock), or reading secrets from your vault. Supports email/password, API key, and SSO authentication methods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[startupbros](https://clawhub.ai/user/startupbros)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to install and configure the Bitwarden CLI, authenticate to a Bitwarden or Vaultwarden vault, manage session state, and retrieve secrets for command-line workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vault session tokens and exported secrets can remain available in persistent shell or tmux sessions.

Mitigation: Lock or log out immediately after use, avoid leaving tmux sessions open, and treat BW_SESSION, BW_CLIENTSECRET, and exported application secrets as live credentials.

Risk: Examples include create and edit commands that can change vault contents.

Mitigation: Require explicit confirmation before running any command that creates, edits, deletes, or otherwise modifies vault items.

Risk: Secret values may be exposed in logs, terminal output, command history, or files.

Mitigation: Avoid logging secrets, avoid writing secrets to disk unless necessary, and prefer short-lived environment variables or direct piping into the consuming command.

## Reference(s):

- [Bitwarden CLI Documentation](https://bitwarden.com/help/cli/)
- [Bitwarden Downloads](https://bitwarden.com/download/)
- [Get Started Guide](references/get-started.md)
- [CLI Examples](references/cli-examples.md)
- [ClawHub Skill Page](https://clawhub.ai/startupbros/skills/bitwarden-vault)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include commands that read vault data, export environment variables, or manage Bitwarden CLI sessions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
