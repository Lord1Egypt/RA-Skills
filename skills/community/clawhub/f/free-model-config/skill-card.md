## Description:

Guides users in selecting and configuring free or credit-based AI models across multiple platforms, with optional multimodal generation and audio and video tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to compare supported AI model platforms, prepare API-compatible model configuration, and get usage guidance. It can also help generate or combine image, video, and audio content through the included workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflows automatically upload local files to public hosts.

Mitigation: Use non-sensitive media until the files and destination are explicitly approved; inspect storyboard paths before running them.

Risk: API keys may be exposed through reports or inadequately protected configuration files and backups.

Mitigation: Keep API keys out of reports and protect configuration files and backups.

Risk: Applying configuration changes can affect existing files, and predictable temporary files may be unsafe.

Mitigation: Preview changes before using --write and replace predictable temporary files. Explicitly select the video model because the documented script default is paid.

## Reference(s):

- [Free-Model Config on ClawHub](https://clawhub.ai/wangjiaocheng/skills/free-model-config)
- [Task catalog](artifact/references/fmc-catalog.md)
- [Method requirements](artifact/references/fmc-requirements.md)
- [Workflow exemplars](artifact/references/fmc-exemplars.md)

## Skill Output:

**Output Type(s):** [Configuration, Guidance, Code, Shell commands, Generated media]

**Output Format:** [Markdown guidance, JSON configuration, code, shell commands, and media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated or combined image, video, and audio assets.]

## Skill Version(s):

1.0.11 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
