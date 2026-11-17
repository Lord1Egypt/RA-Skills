## Description:

Automates Douyin short-video planning and production workflows, including trend collection, content analysis, script generation, optional Kling API video generation, and FFmpeg assembly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felixlam10](https://clawhub.ai/user/felixlam10)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators and content teams use this agent skill to turn client briefs and current Douyin trends into content strategy, short-video scripts, AI-video prompts, and optional generated video assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent scheduled jobs for multi-day content generation.

Mitigation: Review exact dates, task counts, workflow steps, API usage, and removal method before allowing automatic scheduling.

Risk: The workflow may download Douyin media, collect comments, and create transcripts that include sensitive operational data.

Mitigation: Run the skill in a dedicated environment and restrict access to downloaded media, comments, transcripts, and generated outputs.

Risk: Optional automated video generation uses Kling API credentials.

Mitigation: Provide credentials only through environment variables, rotate them if exposed, and avoid sharing them in prompts or logs.

Risk: Broad web and video automation can produce misleading analysis or depend on changing third-party site behavior.

Mitigation: Review generated trend analysis, scripts, shell commands, and video outputs before publishing or scheduling follow-up tasks.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/felixlam10/skills/douyin-video-forge-felix)
- [Browser navigation reference](artifact/references/browser-navigation.md)
- [Douyin algorithm reference](artifact/references/douyin-algorithm.md)
- [Trend analysis reference](artifact/references/trend-analysis.md)
- [Script templates](artifact/references/script-templates.md)
- [Kling prompt guide](artifact/references/kling-prompt-guide.md)
- [Seedance prompt guide](artifact/references/seedance-prompt-guide.md)
- [Kling API site](https://klingai.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown reports, segmented scripts, AI-video prompt blocks, shell commands, JSON helper output, and optional MP4 files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ffmpeg and yt-dlp for core workflows; Python, faster-whisper, and Kling API credentials are optional for transcription and automated video generation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
