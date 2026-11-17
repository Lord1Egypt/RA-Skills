## Description:

Album Pipeline automates AI music album production from concept exploration through songwriting, generation, selection, transcoding, cover and promotional asset creation, platform checks, and final packaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raylanlin](https://clawhub.ai/user/raylanlin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative producers use this skill to coordinate a structured album-production workflow across specialized sub-agents, producing concept documents, song drafts, generation prompts, audio deliverables, cover concepts, promotional materials, and release packaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary says the skill launches broad background workflows and creates many files.

Mitigation: Review the planned workflow before execution and require explicit confirmation before CLI execution, overwrites, or final packaging steps.

Risk: The release security summary says the skill sends prompts, lyrics, images, audio, and video-generation requests to external MiniMax tools.

Mitigation: Review external-service privacy and billing terms before use and avoid submitting confidential, regulated, or unreleased material without approval.

Risk: The release security summary says command templates use user-derived album and track names unsafely.

Mitigation: Validate and quote filename slugs for album and track names before running generated shell commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/raylanlin/skills/album-pipeline)
- [MiniMax CLI](https://github.com/MiniMax-AI/cli)
- [File Contracts](artifact/FILE_CONTRACTS.md)
- [Production Pipeline Review](artifact/docs/production-pipeline-review.md)
- [Example Album Overview](artifact/examples/album-overview.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown documents, plain-text prompts, JSON indexes, shell commands, generated media files, and packaged release assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coordinates multiple sub-agents, creates and updates project files, and may invoke external MiniMax tools for music, image, and video generation.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
