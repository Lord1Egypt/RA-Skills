## Description:

A lightweight AI Agent runtime tool that provides an integrated web management interface, supports multiple LLM providers, and is fully compatible with OpenClaw's skill ecosystem.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yesong-hue](https://clawhub.ai/user/yesong-hue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install and configure a lightweight AI agent runtime with a web interface, multi-provider LLM support, and OpenClaw-compatible agent configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install and update flow can run mutable remote scripts or unverified binaries with broad local authority.

Mitigation: Review the installer before use, prefer a versioned release, verify any available checksum or signature, and avoid administrator or root privileges unless required.

Risk: The local ~/.fastclaw directory may contain API keys, conversations, agent configuration, and long-term memory.

Mitigation: Treat the directory as sensitive, back it up before deletion, and avoid regulated or secret data until storage, authentication, and provider-data handling are clear.

Risk: The runtime connects to external or local LLM providers selected by the user.

Mitigation: Configure only trusted providers and avoid entering sensitive data until provider terms, retention, and access controls are understood.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yesong-hue/skills/ai-agent-runtime)
- [ClawHub homepage metadata](https://clawhub.ai/yesong-Hue/ai-agent-runtime)
- [OpenClaw project](https://github.com/openclaw/openclaw)
- [OpenRouter](https://openrouter.ai)
- [Ollama](https://ollama.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON/Markdown configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct users to install a local runtime, configure LLM provider credentials, and manage local agent files.]

## Skill Version(s):

1.2.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
