## Description:

Anime Drama converts novel text into vertical anime-style short videos by generating a shot script, images, video clips, and an ffmpeg-merged MP4.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricksf](https://clawhub.ai/user/ricksf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to turn story text into short vertical anime-style video drafts using RunningHub AI applications and ffmpeg. It is intended for workflows that can review generated media, external API processing, and local script execution before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted story text could trigger unintended local command execution through the pipeline's command construction.

Mitigation: Review or patch the skill before installation and remove shell=True command construction before running it on untrusted story text.

Risk: The RunningHub API key may be exposed if command output or logs are captured.

Mitigation: Protect RUNNINGHUB_API_KEY, avoid sharing logs from pipeline runs, and rotate the key if logs may already contain it.

Risk: Unpublished drafts and uploaded images are processed by RunningHub.

Mitigation: Avoid sensitive unpublished drafts unless external RunningHub processing is acceptable for the use case.

## Reference(s):

- [Pipeline Usage](artifact/references/pipeline-usage.md)
- [ffmpeg Install](artifact/references/ffmpeg-install.md)
- [RunningHub AI App Notes](artifact/references/runninghub-ai-app-notes.md)
- [ClawHub Skill Page](https://clawhub.ai/ricksf/skills/anime-drama)
- [Skill Homepage](https://github.com/win4r/ClawTeam-OpenClaw)
- [RunningHub Upload API Endpoint](https://www.runninghub.cn/task/openapi/upload)
- [ffmpeg Static Build Release](https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, files]

**Output Format:** [Markdown guidance with shell commands and Python pipeline outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a shot_script.json file plus generated PNG images, MP4 scene clips, and a final vertical 1080x1920 MP4 when the pipeline completes.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
