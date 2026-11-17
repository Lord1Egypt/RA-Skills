## Description:

Process blog content to extract videos and generate GIF previews. Works with blogwatcher, video-frames, and gifgrep skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operations teams use this skill to process blog or RSS feeds, extract embedded video URLs, and generate lightweight GIF previews for quick review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency hygiene concerns may affect reproducibility or production assurance, especially around ffmpeg-static.

Mitigation: Pin dependencies, keep a lockfile, and review the ffmpeg-static package source before relying on the skill in production.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/skills/blog-content-proc)
- [Publisher Profile](https://clawhub.ai/user/terrycarter1985)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with generated video URL lists and GIF preview file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on RSS parsing and ffmpeg-backed GIF generation dependencies.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
