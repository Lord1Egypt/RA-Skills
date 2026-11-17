## Description:

Use when creating complete AI-generated short videos, social videos, promotional videos, narration videos, or script-to-video outputs from a topic, brief, product, article, or approved script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darknoah](https://clawhub.ai/user/darknoah)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and developers use this skill to turn a topic, brief, product, article, or approved script into a complete short-video production workflow. It guides format selection, script confirmation, storyboarding, media sourcing, narration, editing, subtitle generation, music, rendering, and final output checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled media download tools use network access to stock-media providers and can write downloaded assets or raw JSON results to local paths.

Mitigation: Install only where provider network access and local file writes are acceptable; keep downloads in a dedicated media output directory.

Risk: Security evidence flags under-scoped arbitrary URL and file-write behavior in the media download tools.

Mitigation: Avoid passing untrusted URLs or output paths into download commands, and prefer versions that restrict downloads to validated provider asset URLs.

Risk: Provider credentials are required for media searches and downloads.

Mitigation: Use limited-scope API keys, store them locally in config.json or environment variables, and do not paste raw keys into chat.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/darknoah/skills/ai-short-video-workflow)
- [Pexels API](https://api.pexels.com/v1)
- [Pixabay API](https://pixabay.com/api/)
- [Pixabay Videos API](https://pixabay.com/api/videos/)
- [Jamendo API](https://api.jamendo.com/v3.0)
- [Freesound API](https://freesound.org/apiv2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, script and storyboard tables, configuration notes, optional JSON media search results, subtitle files, and rendered video file guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to call stock-media APIs, use local API-key configuration, download media assets, generate ASS subtitles, and render H.264 MP4 outputs after user confirmation checkpoints.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
