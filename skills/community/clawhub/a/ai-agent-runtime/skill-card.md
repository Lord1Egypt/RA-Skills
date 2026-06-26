## Description: <br>
A lightweight AI Agent runtime tool that provides an integrated web management interface, supports multiple LLM providers, and is fully compatible with OpenClaw's skill ecosystem. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yesong-hue](https://clawhub.ai/user/yesong-hue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to deploy and manage a lightweight multi-provider AI agent runtime with a local web interface, SOUL.md-compatible agent configuration, and optional local model support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote one-line installers and downloaded binaries can execute code before the user has reviewed the release contents. <br>
Mitigation: Prefer manual download of a pinned release, verify the source and hash where available, and review installer commands before execution. <br>
Risk: The runtime handles LLM provider API keys and may store credentials or memory under the user's local FastClaw directory. <br>
Mitigation: Use limited-scope API keys, keep the local data directory private, avoid entering confidential data unless the provider is trusted, and periodically inspect or delete apikeys.json and MEMORY.md. <br>
Risk: A local web management interface can expose agent configuration and conversations if the host or port is accessible to untrusted users. <br>
Mitigation: Bind the interface to local access where possible, restrict host access, and avoid running it on shared systems without additional controls. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yesong-Hue/ai-agent-runtime) <br>
- [OpenClaw Project](https://github.com/openclaw/openclaw) <br>
- [FastClaw Releases](https://github.com/fastclaw-ai/fastclaw/releases/latest) <br>
- [OpenRouter](https://openrouter.ai) <br>
- [Ollama](https://ollama.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local runtime setup steps, provider API-key configuration guidance, and agent configuration files.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
