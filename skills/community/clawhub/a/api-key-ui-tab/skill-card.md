## Description:

Vault-backed API key management for OpenClaw with local file-based secret storage, migration from plaintext config, dynamic key discovery, a skills vault-key selector, manual secret creation, and a settings tab.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:


## Use Case:

OpenClaw users and developers use this skill to manage API keys in the Control dashboard, migrate plaintext config values into local file-backed SecretRef entries, and link skill API-key settings to vault keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles real credentials and stores them locally in plaintext JSON protected by file permissions, despite UI language saying encrypted.

Mitigation: Review before installing or enabling with real credentials, restrict access to ~/.openclaw/secrets.json, and do not rely on UI encryption claims.

Risk: Migration behavior can leave plaintext secrets in openclaw.json, especially nested skill or provider keys.

Mitigation: After migration, inspect OpenClaw configuration for remaining plaintext API keys and convert or remove them before use.

Risk: The included reference code can alter auth profiles and skill configuration, including skill installation flows.

Mitigation: Review configuration and auth-profile changes before applying the code, and test in a non-production OpenClaw profile first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maverick-software/skills/api-key-ui-tab)
- [Publisher profile](https://clawhub.ai/user/maverick-software)
- [Skill source overview](artifact/SKILL.md)
- [Installation instructions](artifact/INSTALL_INSTRUCTIONS.md)
- [Vault RPC reference](artifact/reference/secrets-rpc.ts)
- [Skills vault integration reference](artifact/reference/skills-rpc.ts)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown documentation with TypeScript reference code and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focused on OpenClaw API-key and skill configuration workflows; review credential handling before use.]

## Skill Version(s):

3.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
