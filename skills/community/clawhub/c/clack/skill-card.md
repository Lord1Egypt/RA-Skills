## Description:

Clack deploys and manages a self-hosted WebSocket voice relay for OpenClaw that bridges voice input through STT, an OpenClaw agent, and TTS for real-time voice conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fbn3799](https://clawhub.ai/user/fbn3799)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use Clack to install and operate a voice interface for an OpenClaw agent, including secure pairing, provider selection, conversation history, and local or cloud STT/TTS modes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer and service use root-level setup, systemd persistence, and host network configuration.

Mitigation: Review scripts before installation, prefer a dedicated host, and restrict firewall and Tailscale ACLs tightly.

Risk: Relay and gateway tokens grant access to protected voice relay and OpenClaw gateway functions.

Mitigation: Protect and rotate relay and gateway tokens, avoid shared machines, and keep provider API keys in restricted configuration files.

Risk: The update command pulls code and restarts the service.

Mitigation: Review updates before running clack update until the service runs under an unprivileged account with pinned dependencies.

## Reference(s):

- [Clack ClawHub page](https://clawhub.ai/fbn3799/skills/clack)
- [Clack source homepage](https://github.com/fbn3799/clack-skill)
- [Clack app](https://clack-app.com)
- [OpenClaw project](https://github.com/openclaw/openclaw)
- [README](README.md)
- [Full protocol docs](SKILL.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup, management, pairing, update, and troubleshooting instructions for a Linux-hosted voice relay service.]

## Skill Version(s):

1.5.3 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
