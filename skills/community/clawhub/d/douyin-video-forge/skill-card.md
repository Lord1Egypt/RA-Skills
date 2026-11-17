## Description:

Automates Douyin short-video planning and production by collecting trend data, generating scripts and AI-video prompts, optionally calling the Kling API, and stitching vertical video segments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bruce-agnet](https://clawhub.ai/user/bruce-agnet)

### License/Terms of Use:

MIT-0

## Use Case:

Short-video operators, MCN teams, and brand marketers use this skill to gather Douyin trend and competitor signals, turn them into content strategy, generate scripts and prompts, and optionally produce stitched 9:16 videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can browse Douyin, download public videos, run local media tools, call the Kling API, and create recurring jobs.

Mitigation: Require explicit user confirmation before downloads, API calls, and scheduling; review or disable recurring jobs unless unattended generation is intended.

Risk: Untrusted text or arbitrary URLs may be used in download, shell, or API workflows.

Mitigation: Prefer trusted local files and known Douyin URLs, quote shell arguments, and review generated commands before execution.

Risk: Kling API credentials are used from the environment for optional video generation.

Mitigation: Keep credentials in environment variables, avoid pasting secrets into chat, and confirm the intended prompt and spend before each generation batch.

## Reference(s):

- [Douyin Video Forge Skill Page](https://clawhub.ai/bruce-agnet/skills/douyin-video-forge)
- [Douyin Page Navigation Reference](artifact/references/browser-navigation.md)
- [Douyin Trend Analysis Knowledge Base](artifact/references/trend-analysis.md)
- [Douyin Recommendation and Viral-Content Methodology](artifact/references/douyin-algorithm.md)
- [Script Template Knowledge Base](artifact/references/script-templates.md)
- [Kling 3.0 Prompt Guide](artifact/references/kling-prompt-guide.md)
- [Seedance 2.0 Prompt Guide](artifact/references/seedance-prompt-guide.md)
- [Kling API Portal](https://klingai.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown reports, content strategy, scripts, AI-video prompts, inline shell commands, and JSON from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local audio/video file paths and Kling video URLs when optional video generation is enabled.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
