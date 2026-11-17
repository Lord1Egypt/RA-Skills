## Description:

FastClaw is a lightweight AI Agent runtime deployment skill for installing and configuring a web-managed, SOUL.md-compatible multi-model agent environment through the OpenClaw Skills ecosystem.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yesong-hue](https://clawhub.ai/user/yesong-hue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to deploy a lightweight FastClaw AI assistant runtime with a local web UI, SOUL.md-compatible agent configuration, and connections to OpenRouter, OpenAI, Anthropic, Ollama, or custom OpenAI-compatible APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer guidance includes pipe-to-shell commands from mutable remote branches and may be run with elevated privileges.

Mitigation: Prefer manual, version-pinned downloads; inspect installer contents before execution; avoid running curl | bash or irm | iex in an Administrator or root shell.

Risk: Downloaded binaries are described without published checksums or signatures in the supplied evidence.

Mitigation: Use releases with published checksums or signatures when available, and verify artifacts before adding them to PATH.

Risk: FastClaw API keys and local agent data are stored under the user's .fastclaw directory.

Mitigation: Restrict local file access, avoid sharing the directory, and rotate API keys if the directory is exposed.

Risk: The documented cleanup command permanently removes local FastClaw data.

Mitigation: Back up required agent configuration and conversation data before deleting ~/.fastclaw.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/yesong-hue/skills/fastclaw-ai-deployer)
- [ClawHub Package Homepage](https://clawhub.ai/yesong-Hue/fastclaw-ai-deployer)
- [Publisher Profile](https://clawhub.ai/user/yesong-hue)
- [FastClaw Project Reference](https://github.com/fastclaw-ai/fastclaw)
- [OpenClaw Project Reference](https://github.com/openclaw/openclaw)
- [OpenRouter](https://openrouter.ai)
- [Ollama](https://ollama.com)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with shell, PowerShell, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes platform-specific install steps, FastClaw agent configuration templates, and local data path guidance.]

## Skill Version(s):

1.2.0 (source: server release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
