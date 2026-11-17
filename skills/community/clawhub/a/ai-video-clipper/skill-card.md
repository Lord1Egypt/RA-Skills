## Description:

AI视频剪辑Skill helps agents automate local video-editing workflows, including media analysis, clip selection, transitions, audio processing, subtitle generation, effects, and final export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai285384076-droid](https://clawhub.ai/user/ai285384076-droid)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content creators use this skill to turn local video, audio, and image assets into edited videos for short clips, compilations, explainers, Vlogs, and tutorial-style content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broadly process private local media and transcribe speech from selected recordings.

Mitigation: Run it only on explicitly chosen media directories, avoid sensitive recordings unless transcription is intended, and use a dedicated output folder.

Risk: Installation guidance includes ambiguous dependency instructions around Whisper.

Mitigation: Install in a virtual environment with pinned dependencies and prefer the unambiguous `openai-whisper` package.

Risk: Path validation and FFmpeg concat escaping require review before handling untrusted media filenames or analysis JSON.

Mitigation: Treat media filenames and generated analysis JSON as untrusted inputs until path validation and escaping are fixed.

Risk: Running media-processing scripts with elevated privileges increases the impact of unsafe path handling.

Mitigation: Do not run the skill as administrator or root.

## Reference(s):

- [Quickstart](artifact/references/quickstart.md)
- [Default Configuration](artifact/references/default_config.yaml)
- [FFmpeg Guide](artifact/references/ffmpeg_guide.md)
- [FFmpeg Downloads](https://ffmpeg.org/download.html)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown guidance with bash commands, JSON or YAML configuration examples, Python scripts, analysis JSON, and generated video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes local media directories and can produce intermediate analysis, subtitle, audio, effects, and final export files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
