## Description:

Trustless encrypted vault with TOTP auth and clean-room session isolation. Secrets your agent holds but cannot read. Use when user wants to store, retrieve, or manage encrypted secrets securely.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[cmill01](https://clawhub.ai/user/cmill01)

### License/Terms of Use:


## Use Case:

External users and agent developers use Agent SCIF to store and manage encrypted vault entries while keeping the main agent from reading vault contents. The release is a proof-of-concept for agent-blind storage and clean-room relay workflows, not a production secrets manager.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags serious injection, file-scope, temporary-file, and key-persistence risks while the skill manages secrets through a sub-agent and Telegram.

Mitigation: Treat this as a proof-of-concept and use it only in an isolated environment with low-value test secrets until destination validation, sender_id path constraints, temporary-file handling, model-generated code execution, session-key storage, and dependency pinning are fixed.

Risk: Vault protection depends on local files, including a TOTP seed stored on the same machine as encrypted vault data.

Mitigation: Do not treat the TOTP code as a full cryptographic factor against host compromise; protect the host filesystem, delete setup QR files, and use a production secrets manager for high-value secrets.

Risk: Secrets typed into the main chat can enter the main agent context before they are added to the vault.

Mitigation: Avoid pasting real secrets into the main chat; use stdin-based entry handling or a direct clean-room input path before using sensitive values.

## Reference(s):

- [ClawHub Agent SCIF skill page](https://clawhub.ai/cmill01/skills/agent-scif)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown instructions with inline shell commands and generated vault files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Python dependencies and an out-of-band messaging channel for clean-room responses.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
