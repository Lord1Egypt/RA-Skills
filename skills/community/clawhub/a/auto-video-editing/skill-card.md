## Description:

Automated video editing skill for talk/vlog/standup videos that helps an agent extract audio, transcribe speech, split videos into sentence clips, burn subtitles, merge selected clips, generate cover titles, and add chapter timeline bars.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxazure](https://clawhub.ai/user/maxazure)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and agent operators use this skill to automate short-form video editing workflows for talk, vlog, standup, and oral presentation videos. It guides an agent through local media processing tasks including transcription, sentence-level clipping, subtitle burn-in, clip selection, final merge, cover generation, and chapter timeline creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local media-processing commands and generated outputs can overwrite existing files when paths are reused.

Mitigation: Choose output paths deliberately, review command targets before execution, and keep original media files separate from generated output directories.

Risk: Dependency installation and package-manager commands can affect the host environment, especially when run with elevated privileges.

Mitigation: Install Python dependencies in a virtual environment, avoid administrator execution for pip or the skill, and review sudo package-manager commands before running them.

Risk: Whisper models, fonts, or mirrored package indexes may involve network downloads from third-party services.

Mitigation: Use trusted package indexes, prefer pinned dependencies where practical, and review mirror settings before downloading models or fonts.

Risk: Transcription and clipping quality depends on source audio, model selection, hardware support, fonts, and FFmpeg capabilities.

Mitigation: Run the bundled environment diagnostic first, inspect and correct transcript JSON before editing, and review final media for subtitle, timing, and chapter accuracy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maxazure/skills/auto-video-editing)
- [Publisher profile](https://clawhub.ai/user/maxazure)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, text, markdown]

**Output Format:** [Markdown guidance with inline shell commands and JSON transcript references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local media-processing guidance and commands; generated video, audio, subtitle, transcript, cover, and chapter files are written by the bundled scripts.]

## Skill Version(s):

1.2.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
