## Description:

视频自动字幕生成器，批量为视频生成字幕文件（SRT/VTT），结合视频帧提取和语音转文字，预览模式和撤销功能！

This skill is ready for commercial/non-commercial use.

## Publisher:

[utopiabenben](https://clawhub.ai/user/utopiabenben)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media operators use this skill to generate SRT or VTT subtitle files for batches of local video files using audio extraction and OpenAI Whisper transcription or translation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File restore and output handling can overwrite user-writable files in unsafe directories.

Mitigation: Run the tool only in trusted directories, review generated paths before execution, and avoid --undo in shared or attacker-writable folders until restore handling is hardened.

Risk: Extracted audio is sent to OpenAI for transcription.

Mitigation: Process only media approved for external transcription and configure OPENAI_API_KEY in an isolated environment.

Risk: Dependencies are installed without pinned versions.

Mitigation: Install in an isolated environment and pin openai and pydub versions for managed deployments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/utopiabenben/skills/auto-subtitle)
- [Publisher Profile](https://clawhub.ai/user/utopiabenben)

## Skill Output:

**Output Type(s):** [text, files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated subtitle files in SRT or VTT format]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENAI_API_KEY, Python 3.7+, ffmpeg, openai, and pydub; supports preview mode and undo for the most recent subtitle operation.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
