## Description: <br>
Vault-backed API Keys management for OpenClaw. Secure file-based secret storage with one-click migration from plaintext config, dynamic key discovery, vault key selector for skills, manual secret creation, and plugin-registered settings tab. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to manage API keys through a vault-backed settings UI, migrate plaintext keys into local secret references, and link skills to vault keys without exposing raw values in configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles high-value API credentials while the security evidence says local protection may be overstated. <br>
Mitigation: Install only on a trusted machine, treat the vault as a local permission-protected JSON secrets file rather than proven encrypted storage, and restrict access to the local OpenClaw files. <br>
Risk: Migration and auth-profile controls can change or delete local credential state. <br>
Mitigation: Back up openclaw.json and secrets.json before migration, verify compatibility with the installed OpenClaw version, and use delete or reset controls carefully. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/maverick-software/api-key-ui-tab) <br>
- [Installation instructions](INSTALL_INSTRUCTIONS.md) <br>
- [API keys controller reference](reference/apikeys-controller.ts) <br>
- [API keys view reference](reference/apikeys-views.ts) <br>
- [Secrets RPC reference](reference/secrets-rpc.ts) <br>
- [Skills controller reference](reference/skills-controller.ts) <br>
- [Skills RPC reference](reference/skills-rpc.ts) <br>
- [Skills status reference](reference/skills-status.ts) <br>
- [Skills view reference](reference/skills-views.ts) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with TypeScript reference code and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces OpenClaw installation and integration guidance; the release artifact includes reference implementation files rather than a standalone executable.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
