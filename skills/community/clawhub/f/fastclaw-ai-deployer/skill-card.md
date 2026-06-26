## Description: <br>
FastClaw是一款轻量级AI Agent运行时工具，支持通过OpenClaw Skills生态安装，提供内置Web界面、SOUL.md兼容、多模型支持等功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yesong-hue](https://clawhub.ai/user/yesong-hue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to install and configure a lightweight FastClaw AI agent runtime with a local web interface, SOUL.md-compatible agent templates, and multi-provider model setup guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote installer commands can execute downloaded shell or PowerShell content. <br>
Mitigation: Review the installer source and verify trust in the FastClaw GitHub source before running one-line install commands. <br>
Risk: FastClaw configuration may store API keys and provider settings under ~/.fastclaw. <br>
Mitigation: Treat ~/.fastclaw as sensitive, restrict local access, and avoid committing or sharing files from that directory. <br>
Risk: Saved agent memory may retain personal, project, or confidential information. <br>
Mitigation: Review MEMORY.md periodically, remove entries that should not be retained, and avoid sending confidential data to hosted LLM providers unless their policies meet your needs. <br>


## Reference(s): <br>
- [ClawHub FastClaw AI部署工具 Release Page](https://clawhub.ai/yesong-hue/fastclaw-ai-deployer) <br>
- [FastClaw GitHub Project](https://github.com/fastclaw-ai/fastclaw) <br>
- [OpenClaw GitHub Project](https://github.com/openclaw/openclaw) <br>
- [OpenRouter](https://openrouter.ai) <br>
- [Ollama](https://ollama.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with shell commands, configuration paths, and JSON templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide users through installing FastClaw, configuring API keys, editing SOUL.md, and managing local agent files.] <br>

## Skill Version(s): <br>
1.2.0 (source: ClawHub release metadata; artifact frontmatter lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
