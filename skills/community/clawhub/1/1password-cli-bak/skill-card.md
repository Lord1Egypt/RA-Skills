## Description: <br>
Securely access and manage secrets using the 1Password CLI with a service account token for reading, writing, editing, and deleting items in a dedicated vault. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reiy-leo](https://clawhub.ai/user/reiy-leo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate the 1Password CLI with a narrowly scoped service account for vault and item workflows. It supports authentication checks, vault listing, and controlled secret read, create, edit, and delete operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents direct ability to read, create, edit, cache, and delete secrets through the 1Password CLI. <br>
Mitigation: Use a dedicated service account with minimum vault permissions, avoid personal or production vaults, and require explicit approval before create, edit, or delete actions. <br>
Risk: Secret values or service account tokens could be exposed in logs, console output, or cached results. <br>
Mitigation: Do not print OP_SERVICE_ACCOUNT_TOKEN or retrieved secrets, avoid caching secret values, and rotate or revoke the service account token when work is complete. <br>


## Reference(s): <br>
- [1Password CLI get started](https://developer.1password.com/docs/cli/get-started) <br>
- [1Password Developer Portal](https://developer.1password.com/) <br>
- [ClawHub skill page](https://clawhub.ai/reiy-leo/1password-cli-bak) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require OP_SERVICE_ACCOUNT_TOKEN and should avoid exposing token or secret values.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
