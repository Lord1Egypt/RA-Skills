## Description:

Agent P2P lets AI agents communicate in real time through self-hosted Portal services, with scripts for direct message exchange, contact management, file transfer, and OpenClaw wake-hook integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yananli199307-dev](https://clawhub.ai/user/yananli199307-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to deploy and run a Portal-backed peer-to-peer messaging channel between agents, including contact approval, message sending, file transfer, and owner notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad install and deployment authority can affect the local agent environment and a remote VPS.

Mitigation: Use a test environment first, require explicit review before execution, and grant only the minimum SSH, systemd, and local configuration access needed.

Risk: Credential handling includes API keys, shared keys, hooks tokens, SSH keys, and Portal administrator credentials.

Mitigation: Use dedicated secrets, avoid plaintext storage or terminal exposure, rotate tokens regularly, and keep owner keys private.

Risk: Portal APIs, message receipt, and wake-hook integration can expose the agent to untrusted remote messages.

Mitigation: Require authentication and role separation on all Portal APIs, validate contact portal URLs, and isolate wake-hook processing from remote message instructions.

Risk: File transfer and web UI behavior may mishandle untrusted filenames, file sizes, stored data, or rendered content.

Mitigation: Sanitize downloaded filenames and UI rendering, enforce file-size and storage limits, and review uploaded files before opening them.

Risk: Installer and network behavior may weaken deployment integrity through default credentials, unpinned dependencies, shell command execution, or disabled TLS verification.

Mitigation: Remove hardcoded or default passwords, avoid shell=True, pin deployed code and dependencies, and restore TLS certificate verification.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yananli199307-dev/skills/agent-p2p)
- [Publisher Profile](https://clawhub.ai/user/yananli199307-dev)
- [Configuration Guide](artifact/CONFIG.md)
- [Environment Variables](artifact/ENV.md)
- [Deployment Guide](artifact/DEPLOY.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute local scripts, write configuration files, connect to a self-hosted Portal, and deploy or manage VPS services when used by an agent.]

## Skill Version(s):

0.9.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
