## Description: <br>
Generate high-quality music on Apple Silicon Macs using ACE-Step 1.5 with MLX backend, supporting custom prompts, durations, and output formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RichmanDP](https://clawhub.ai/user/RichmanDP) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and local-agent users on Apple Silicon Macs use this skill to install or call ACE-Step 1.5, generate audio from text prompts, and optionally route generated files or notifications through local or messaging workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installer and helper scripts can execute local shell commands and download external model or project assets. <br>
Mitigation: Review scripts before running them, prefer documented manual install steps, and run inside a dedicated virtual environment. <br>
Risk: The localhost API can generate files from caller-supplied prompts and output paths. <br>
Mitigation: Bind and use the API only for trusted local callers, and keep generated output paths inside a dedicated music directory. <br>
Risk: Optional Telegram, Discord, and Feishu workflows can share prompts or generated audio with third-party services. <br>
Mitigation: Use messaging integrations only when the prompt and generated file are acceptable to share with the selected service. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/RichmanDP/ace-step-music) <br>
- [ACE-Step Project](https://github.com/ace-step/ACE-Step) <br>
- [ACE-Step 1.5 Model](https://huggingface.co/ACE-Step/Ace-Step1.5) <br>
- [Apple MLX Framework](https://github.com/ml-explore/mlx) <br>
- [Skill Usage Documentation](artifact/AGENT_USAGE.md) <br>
- [Music Sending Guide](artifact/SEND_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, audio files, guidance] <br>
**Output Format:** [Markdown guidance with bash, Python, JSON, and Docker configuration examples; generated music is saved as WAV audio.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets local macOS Apple Silicon environments; outputs default to ~/Music/ACE-Step and can be routed through optional messaging integrations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
