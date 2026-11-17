## Description:

Create complete AI music videos from local audio or public audio URLs with 1-7 reference images. Use for single-track or batch music video production, creative direction, task monitoring, and result downloads through the official BizMuse CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bizmuse-ai](https://clawhub.ai/user/bizmuse-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and production teams use this skill to generate single-track or batch AI music videos from finished audio, visual references, and creative direction through BizMuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends audio, reference images, prompts, and generated media to the external BizMuse service.

Mitigation: Confirm the user has rights to upload and process supplied media, and upload only material required for the requested video.

Risk: Improper API key handling could expose BizMuse account credentials.

Mitigation: Configure the API key only through the BizMuse CLI in the user's terminal; do not paste, print, repeat, or store credentials in chat or project files.

Risk: The skill depends on a locally installed npm CLI package and paid service credits.

Mitigation: Install only if the BizMuse package source is trusted, avoid sudo for global installation, and verify account credits before generation.

Risk: Asynchronous generation can remain pending or fail, which may lead to misleading completion reports.

Mitigation: Retain task IDs, check status no more frequently than every 30 seconds, stop polling after 30 minutes, and never invent successful media URLs.

## Reference(s):

- [BizMuse Skill Documentation](https://bizmuse.ai/skill)
- [BizMuse Product](https://bizmuse.ai)
- [BizMuse Pricing](https://bizmuse.ai/pricing)
- [ClawHub Skill Page](https://clawhub.ai/bizmuse-ai/skills/bizmuse-music-video)
- [Setup and Input Requirements](references/setup.md)
- [Supported Model and Controls](references/models.md)
- [Music Video Prompt Guide](references/prompts.md)
- [Error Handling](references/errors.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task IDs, status, video and cover URLs, download paths, batch manifests, per-file failures, and actionable provider or account errors.]

## Skill Version(s):

1.1.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
