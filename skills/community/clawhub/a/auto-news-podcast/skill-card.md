## Description:

Auto News Podcast generates news podcast packages from user-provided topics by searching news, summarizing articles, creating broadcast scripts, selecting cover images, and producing TTS audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiazengtian](https://clawhub.ai/user/jiazengtian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and content teams use this skill to turn a topic or batch of topics into news briefings with summaries, broadcast scripts, cover images, audio, and optional deep-dive segments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads OpenClaw configuration and environment API keys.

Mitigation: Use dedicated low-privilege API keys and review local configuration before running the skill.

Risk: The skill sends user topics and fetched article content to external search, model, image, and TTS services.

Mitigation: Avoid sensitive topics or private source material, and run it behind a network sandbox that blocks localhost, private networks, and metadata services.

Risk: The skill writes generated files under the OpenClaw workspace and can run other installed skill scripts for audio generation.

Mitigation: Review the output directory and installed companion skills before execution.

## Reference(s):

- [Auto News Podcast on ClawHub](https://clawhub.ai/jiazengtian/skills/auto-news-podcast)
- [Unsplash Developers](https://unsplash.com/developers)
- [Unsplash Search Photos API](https://api.unsplash.com/search/photos)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration]

**Output Format:** [Workspace files including Markdown summaries, plain-text scripts, title and label text, JPG cover images, MP3 audio, and batch reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes timestamped output directories under workspace/news; batch mode also produces a configuration list and generation summary.]

## Skill Version(s):

1.0.12 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
