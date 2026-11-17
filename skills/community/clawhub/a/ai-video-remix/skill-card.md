## Description:

AI-driven video remix generator that uses ShotAI semantic search, optional LLM planning, and Remotion rendering to produce styled video compositions from a user's local video library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abu-shotai](https://clawhub.ai/user/abu-shotai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to ask an agent for travel vlogs, sports highlights, nature montages, and other styled cuts from local footage that has already been imported and indexed in ShotAI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed package asks users to clone and execute unpinned external runtime code that was not included in the package.

Mitigation: Review the external repository before use and prefer a pinned commit or reviewed release.

Risk: The runtime processes local video files and uses ShotAI and optional LLM credentials.

Mitigation: Run it in a limited workspace and provide only the minimum credentials needed for the selected ShotAI and LLM providers.

Risk: Optional background music download can access YouTube through yt-dlp.

Mitigation: Use a local MP3 with --bgm or BGM_PATH to avoid YouTube access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/abu-shotai/skills/ai-video-remix)
- [AI Video Remix Source Repository](https://github.com/abu-ShotAI/ai-video-remix)
- [ShotAI](https://www.shotai.io)
- [Setup Guide](references/setup.md)
- [Configuration Reference](references/config.md)
- [Video Quality Tuning Guide](references/tuning.md)
- [Adding a New Composition](references/composition-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill is instruction-only; rendered MP4 video output is produced by separately cloned runtime code.]

## Skill Version(s):

0.1.3 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
