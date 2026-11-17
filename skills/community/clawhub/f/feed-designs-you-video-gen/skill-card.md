## Description:

Create vertical algorithm-control shorts: five equal caption beats across the runtime, UI/data-stream montage (WeryAI). Use for attention-economy critique, doomscroll hooks, or feed-steering rhetoric. Use when the user says the app chooses for them. SEO: algorithm control video; feed manipulation video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and agent users use this skill to generate vertical short-video prompts and WeryAI video jobs for rhetorical critiques of algorithmic feeds, doomscrolling, and feed manipulation. It supports text-to-video, image-to-video, and limited multi-image workflows with five caption windows timed to the selected duration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts and any supplied image URLs to WeryAI for video generation.

Mitigation: Use only public HTTPS image URLs and avoid sensitive or private content in prompts and images.

Risk: Video generation uses a paid WeryAI API key.

Mitigation: Install and run only where WeryAI usage costs are acceptable and keep WERYAI_API_KEY secret.

Risk: The local script does not enforce every documented image URL and model compatibility rule before submission.

Mitigation: Confirm the expanded prompt, model, duration, aspect ratio, resolution, and image inputs before running generation.

Risk: Algorithm-control messaging could be read as factual claims about named platforms or people if over-specified.

Mitigation: Keep outputs framed as system critique or fiction unless the user provides substantiated factual context, and avoid targeting named individuals.

## Reference(s):

- [WeryAI video CLI and JSON reference](resources/WERYAI_VIDEO_API.md)
- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/feed-designs-you-video-gen)
- [Publisher profile](https://clawhub.ai/user/zoucdr)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON CLI payloads and final video links or structured JSON errors]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WERYAI_API_KEY, Node.js 18+, public HTTPS image URLs for image inputs, and WeryAI-compatible model parameters.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
