## Description:

Set up and use Bitwarden CLI (bw) for installation, login or unlock workflows, and vault secret retrieval with email/password, API key, or SSO authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[startupbros](https://clawhub.ai/user/startupbros)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to install and operate the Bitwarden CLI, authenticate to a vault, and retrieve secrets for local workflows or automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vault secrets may be exposed if commands print passwords, TOTP codes, item JSON, or secret environment variables in shared logs or chat.

Mitigation: Review commands before execution, avoid asking an agent to print secrets, and pass only narrowly scoped values directly to the consuming command.

Risk: Persistent shell sessions and BW_SESSION can keep a vault unlocked longer than needed.

Mitigation: Use trusted sessions only, run bw lock when work is complete, and unset BW_SESSION and other secret variables promptly.

Risk: Examples that create or edit vault records, or download attachments, can modify vault data or write sensitive files to disk.

Mitigation: Require explicit confirmation for create, edit, and download actions, and avoid writing vault material to disk unless necessary.

## Reference(s):

- [Bitwarden CLI documentation](https://bitwarden.com/help/cli/)
- [Bitwarden downloads](https://bitwarden.com/download/)
- [Get Started Guide](references/get-started.md)
- [CLI Examples](references/cli-examples.md)
- [ClawHub skill page](https://clawhub.ai/startupbros/skills/bw-vault)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may retrieve or handle sensitive vault data and should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
