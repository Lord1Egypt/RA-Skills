## Description:

Generate high-quality music on Apple Silicon Macs using ACE-Step 1.5 with an MLX backend, supporting custom prompts, durations, and output formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richmandp](https://clawhub.ai/user/richmandp)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to install and run ACE-Step 1.5 on Apple Silicon Macs, generate music from text prompts, and expose local command, Python, or HTTP interfaces for agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer and deployment scripts can execute high-impact local setup steps.

Mitigation: Review scripts before running them, avoid curl-to-bash execution, and use a dedicated virtual environment.

Risk: Model and dependency downloads may change over time or be tampered with in transit or at the source.

Mitigation: Pin dependency versions and verify downloaded artifacts with trusted hashes where possible.

Risk: The local HTTP API or Docker deployment could expose generation controls beyond the intended machine.

Mitigation: Bind services to localhost, avoid exposing Docker or HTTP ports externally, and add authentication before agent-to-agent use.

Risk: Generated audio, prompts, chat IDs, tokens, or webhook URLs may be sent to external services.

Mitigation: Share through Telegram, Discord, or Feishu only when intentional, and keep credentials in protected environment variables.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/richmandp/skills/ace-step-music)
- [ACE-Step 1.5 GitHub Project](https://github.com/ace-step/ACE-Step-1.5)
- [ACE-Step 1.5 Hugging Face Model](https://huggingface.co/ace-step/ACE-Step-1.5)
- [Apple MLX Framework](https://github.com/ml-explore/mlx)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Bash, Python, YAML, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local audio file paths and commands for optional sharing through external messaging services.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
