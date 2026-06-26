## Description: <br>
Securely access and manage secrets with the 1Password CLI using a service account token for vault operations such as reading, creating, editing, and deleting items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sichengchen](https://clawhub.ai/user/sichengchen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to configure an agent for controlled 1Password vault access through the `op` CLI. It supports common secret-management workflows, including authentication checks, vault listing, item reads, item creation, edits, and deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A service account token can allow an agent to read or change secrets in accessible 1Password vaults. <br>
Mitigation: Use a dedicated vault, grant least-privilege access, and keep OP_SERVICE_ACCOUNT_TOKEN out of logs and repositories. <br>
Risk: Create, edit, or delete commands can modify or remove stored secrets. <br>
Mitigation: Require explicit confirmation before mutation commands and specify the target vault with --vault. <br>
Risk: Retrieved secret values can be exposed through console output or transcripts. <br>
Mitigation: Do not print service account tokens or retrieved secrets unless the operator explicitly requests disclosure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sichengchen/1password-cli) <br>
- [1Password CLI get started](https://developer.1password.com/docs/cli/get-started) <br>
- [1Password Developer Portal](https://developer.1password.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the 1Password CLI and an OP_SERVICE_ACCOUNT_TOKEN in the execution environment.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
