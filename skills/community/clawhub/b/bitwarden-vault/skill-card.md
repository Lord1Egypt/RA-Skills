## Description: <br>
Set up and operate Bitwarden CLI (bw) to install the CLI, authenticate, unlock vault sessions, and retrieve vault secrets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[StartupBros](https://clawhub.ai/user/StartupBros) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to install and run Bitwarden CLI for authenticated vault access, including reading passwords, secure notes, TOTP codes, custom fields, and self-hosted Vaultwarden secrets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vault access can expose passwords, notes, TOTP codes, API keys, session tokens, and downloaded attachments. <br>
Mitigation: Keep requests narrow, avoid printing or logging secrets, avoid unnecessary disk writes, and clean up any files created from vault attachments. <br>
Risk: Exported BW_SESSION values can continue to decrypt vault data until the vault is locked or the session is logged out. <br>
Mitigation: Use a dedicated tmux session only for the task, avoid storing session tokens in shell profiles or CI logs, and run bw lock or bw logout when finished. <br>


## Reference(s): <br>
- [Bitwarden CLI documentation](https://bitwarden.com/help/cli/) <br>
- [Bitwarden downloads](https://bitwarden.com/download/) <br>
- [Get Started Guide](references/get-started.md) <br>
- [CLI Examples](references/cli-examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/StartupBros/bitwarden-vault) <br>
- [Publisher profile](https://clawhub.ai/user/StartupBros) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Bitwarden CLI commands, tmux session steps, environment variable guidance, and JSON-processing examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
