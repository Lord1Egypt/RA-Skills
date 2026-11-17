## Description:

Automatically generates and saves alternative perspectives from a secondary LLM for every user message to enhance reasoning and response quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dannydvm](https://clawhub.ai/user/dannydvm)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Dual-Brain to run a secondary LLM that watches OpenClaw user messages, writes short per-agent perspective files, and lets the primary agent consider those notes before responding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The daemon may send conversation excerpts, and optional memory context, to a configured external LLM provider.

Mitigation: Prefer local Ollama for sensitive workflows, review provider data handling before using remote providers, and configure ownerIds narrowly.

Risk: The tool can run as a persistent background service that watches agent conversation files.

Mitigation: Run it in foreground first, review the watched scope and configuration, and install a system service only when persistent operation is needed.

Risk: API keys may be stored in plaintext configuration.

Mitigation: Protect the configuration file with restrictive permissions, avoid unnecessary remote-provider keys, and rotate keys if the file is exposed.

Risk: Generated perspective files can contain incorrect or misleading advice.

Mitigation: Treat perspectives as untrusted suggestions and require the primary agent or user to evaluate them before acting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dannydvm/skills/dual-brain)
- [README](README.md)
- [Quick Start Guide](QUICKSTART.md)
- [Agent Skill Instructions](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown perspective files with shell command and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces short per-agent latest-perspective files and CLI guidance; default perspective length is controlled by maxTokens.]

## Skill Version(s):

0.1.1 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
