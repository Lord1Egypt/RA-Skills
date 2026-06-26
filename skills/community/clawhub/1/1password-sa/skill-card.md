## Description: <br>
Securely inject secrets from 1Password into agent workflows using service accounts with op run and .env.tpl as the primary pattern, op read as a fallback, and hardened security guidance for credential handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[in-liberty420](https://clawhub.ai/user/in-liberty420) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to access API keys, credentials, and other 1Password secrets without exposing values in chat, logs, shell history, or process arguments. It provides safe command patterns for service-account authentication, secret injection, fallback reads, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: 1Password service-account tokens can expose real secrets if leaked. <br>
Mitigation: Use least-privilege vault access, keep tokens out of chat, logs, shell history, and repositories, and rotate or revoke any token that may have been exposed. <br>
Risk: Diagnostic commands can reveal account emails, vault names, item IDs, URLs, and other sensitive metadata. <br>
Mitigation: Treat diagnostic output as sensitive and avoid recording or logging it in agent sessions. <br>
Risk: Unsafe CLI patterns can print or persist secrets. <br>
Mitigation: Prefer `op run` with masking enabled, avoid `--no-masking`, `--reveal`, `set -x`, verbose curl output, raw stdout reads, and command-line secret arguments. <br>


## Reference(s): <br>
- [1Password CLI Get Started](https://developer.1password.com/docs/cli/get-started/) <br>
- [Get Started](references/get-started.md) <br>
- [CLI Examples](references/cli-examples.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash command examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the 1Password CLI binary (`op`) and an `OP_SERVICE_ACCOUNT_TOKEN` supplied from a secure store.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
