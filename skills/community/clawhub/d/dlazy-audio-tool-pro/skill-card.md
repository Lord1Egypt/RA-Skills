## Description:

音频生成工具-专业版帮助代理使用 dlazy CLI 和外部音频 API 生成 TTS、语音克隆、原创音乐、音效和多角色对话输出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, content teams, and developers use this skill to orchestrate professional audio generation workflows, including narration, cloned voices, music, sound effects, dialogue scenes, and chained batch processing. It is intended for authorized audio production rather than copyrighted media processing or unrelated media conversion tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may upload voice samples to external services for cloning.

Mitigation: Use only authorized voice samples, avoid sensitive recordings, and review third-party service terms before use.

Risk: The skill requires a third-party CLI, API credentials, command execution, and file writes.

Mitigation: Install the CLI from trusted sources, store API keys outside prompts and source files, and review generated commands before execution.

Risk: The activation scope is broader than the stated audio-generation purpose.

Mitigation: Use the skill for audio generation workflows only and route generic video, media conversion, or unrelated file-processing requests to narrower tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/dlazy-audio-tool-pro)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe generated audio URLs, local output files, execution logs, and structured status responses.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
