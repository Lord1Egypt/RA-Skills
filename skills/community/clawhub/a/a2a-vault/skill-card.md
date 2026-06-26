## Description: <br>
Zero-knowledge secrets management via PassBox - store, retrieve, rotate, and inject credentials securely. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Paparusi](https://clawhub.ai/user/Paparusi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to manage PassBox vault secrets, compare or import .env files, rotate credentials, and inject approved credentials into other tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent high-impact access to credentials. <br>
Mitigation: Install only when the A2A plugin and PassBox provider are trusted, and require explicit approval before retrieving, deleting, rotating, or injecting credentials. <br>
Risk: Importing local .env files can move sensitive or unintended values into a vault. <br>
Mitigation: Review .env contents before import and start with non-production vaults. <br>
Risk: Credential operations may affect the wrong vault or environment. <br>
Mitigation: Verify vault and environment names before executing credential retrieval, rotation, deletion, import, or injection workflows. <br>


## Reference(s): <br>
- [A2A Vault on ClawHub](https://clawhub.ai/Paparusi/a2a-vault) <br>
- [Publisher profile](https://clawhub.ai/user/Paparusi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with tool-call examples and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose credential retrieval, storage, rotation, deletion, .env import, and secret injection workflows.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
