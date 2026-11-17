## Description:

Ai Video Pipeline guides an agent from a user short-video idea through script drafting, human confirmation, TTS, background music, generated video clips, subtitles, and MP4 assembly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mydearzsy](https://clawhub.ai/user/mydearzsy)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to turn short-video ideas or manuscripts into confirmed scripts and generated MP4 assets with narration, background music, subtitles, and AI-generated clips. The workflow is designed for agent-assisted Chinese short-video production with human approval before media generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video scripts, prompts, generated media, and API-authenticated requests are sent to named third-party services.

Mitigation: Use the skill only with content and provider terms appropriate for those services, and avoid sensitive or regulated content unless provider and Feishu handling policies allow it.

Risk: The default work directory is /tmp/video-poc, which can be inappropriate in shared environments.

Mitigation: Use a private per-job work directory and avoid reusing shared temporary paths for user content or generated media.

Risk: Untrusted output paths or filenames can increase local file handling risk.

Mitigation: Use fixed, trusted output directories and validate user-supplied filenames before running the media pipeline.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mydearzsy/skills/ai-video-pipeline)
- [Volcengine Visual Intelligence documentation](https://www.volcengine.com/docs/85621)
- [MiniMax music generation API endpoint](https://api.minimaxi.com/v1/music_generation)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown and text guidance with inline shell commands and generated MP4 files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured third-party media service credentials and local video tooling.]

## Skill Version(s):

3.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
