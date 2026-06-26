## Description: <br>
Interact with Bitwarden password manager using the bw CLI for authentication, vault item management, password and passphrase generation, organization operations, and Send workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0x7466](https://clawhub.ai/user/0x7466) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technical users use this skill to operate Bitwarden or Vaultwarden through the bw CLI, including unlock/login flows, vault reads and writes, imports and exports, Sends, and organization administration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable broad agent access to Bitwarden vault contents and credentials. <br>
Mitigation: Install only when an agent is intentionally allowed to operate the vault, and prefer interactive unlock or short-lived secrets. <br>
Risk: Vault exports, deletes, Sends, organization or device approvals, and bw serve can expose or alter sensitive account data. <br>
Mitigation: Require explicit approval before running these operations. <br>
Risk: Raw exports, session keys, passwords, or retrieved secrets may be exposed through command output or logs. <br>
Mitigation: Avoid raw exports and do not log BW_SESSION, BW_PASSWORD, or retrieved secret values. <br>


## Reference(s): <br>
- [Bitwarden CLI documentation](https://bitwarden.com/help/cli/) <br>
- [Bitwarden CLI documentation markdown](https://bitwarden.com/help/cli.md) <br>
- [Bitwarden personal API key documentation](https://bitwarden.com/help/personal-api-key/) <br>
- [Bitwarden CLI command reference](references/commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that retrieve, modify, export, or delete password-vault data.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
