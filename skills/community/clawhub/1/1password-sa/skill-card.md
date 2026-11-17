## Description:

Securely inject secrets from 1Password into agent workflows using service accounts with op run and .env.tpl as the primary pattern, op read as a fallback, and hardened rules for authentication, permissions, and secret handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[in-liberty420](https://clawhub.ai/user/in-liberty420)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to retrieve and inject 1Password-managed API keys, credentials, and other secrets into command workflows while minimizing secret exposure in logs, process arguments, and generated responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may expose secrets by printing command output, dumping environment variables, enabling shell tracing, or passing secrets as command-line arguments.

Mitigation: Use op run with .env.tpl where possible, keep masking enabled, avoid set -x and verbose logging, and never include secret values in chat, logs, tool output, or agent responses.

Risk: A broadly scoped or mishandled 1Password service account can grant more vault or item access than the workflow needs.

Mitigation: Scope the service account to the minimum required vaults and items, store OP_SERVICE_ACCOUNT_TOKEN in a secure store, unset it after use, and rotate it if expired or revoked.

Risk: Untrusted vault, item, field, or .env.tpl input can alter command behavior or expose secret reference structure.

Mitigation: Validate dynamic names, quote shell variables, reject dangerous metacharacters and dangerous environment variable names, restrict .env.tpl permissions, and avoid accepting templates from untrusted sources.

Risk: Diagnostic commands can reveal sensitive metadata such as account emails, vault names, item IDs, and URLs.

Mitigation: Treat diagnostic output as sensitive in logged or recorded sessions and prefer low-impact checks only when needed for troubleshooting.

## Reference(s):

- [1Password CLI get started](https://developer.1password.com/docs/cli/get-started/)
- [get-started.md](references/get-started.md)
- [cli-examples.md](references/cli-examples.md)
- [troubleshooting.md](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the 1Password CLI op binary and OP_SERVICE_ACCOUNT_TOKEN for service-account workflows.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
