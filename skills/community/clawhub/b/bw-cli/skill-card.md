## Description:

Interact with the Bitwarden password manager using the bw CLI for authentication, vault operations, password and passphrase generation, organization management, and Bitwarden Send workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0x7466](https://clawhub.ai/user/0x7466)

### License/Terms of Use:


## Use Case:

Developers, operators, and agent users use this skill as a command reference for working with Bitwarden or Vaultwarden vaults through the bw CLI, including login, unlock, item management, exports, and sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may encourage persistent plaintext storage or shell auto-loading of password manager credentials.

Mitigation: Prefer interactive unlocks or an OS-backed secret manager, and do not keep master passwords in workspace files or auto-sourced shell startup files.

Risk: Commands can expose, export, delete, or share sensitive vault data.

Mitigation: Review commands before execution, avoid raw or full exports unless strictly required, and use reversible operations where available.

Risk: Running the bw REST API server can expand local access to vault operations.

Mitigation: Run bw serve only on localhost and only for the shortest time needed.

## Reference(s):

- [Bitwarden CLI documentation](https://bitwarden.com/help/cli/)
- [Bitwarden CLI markdown documentation](https://bitwarden.com/help/cli.md)
- [Bitwarden personal API key documentation](https://bitwarden.com/help/personal-api-key/)
- [Bitwarden CLI command reference](references/commands.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that access or modify password manager data; review before execution.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
