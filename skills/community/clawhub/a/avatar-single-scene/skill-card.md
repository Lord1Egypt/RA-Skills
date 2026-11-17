## Description:

Guides the creation of one speaking-avatar video, with intake and approval gates before generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pruna-ai](https://clawhub.ai/user/pruna-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and marketing teams use this skill to plan and produce one host-on-camera video from an approved portrait and spoken script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded or generated portraits, audio, and scripts are sent to Pruna APIs.

Mitigation: Review the media and script for sensitive content and obtain permission before uploading.

Risk: Paid avatar generation can incur charges or produce an unwanted clip.

Mitigation: Require explicit approval of the full script and plan, then the still, before starting one video job.

Risk: Installing prerequisite skills through the skills CLI introduces third-party dependencies.

Mitigation: Review the PrunaAI skill package source and use pinned, trusted CLI and skill versions.

## Reference(s):

- [avatar-single-scene on ClawHub](https://clawhub.ai/pruna-ai/skills/avatar-single-scene)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with a script, production plan, approval checkpoints, and generation instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [After approval, the workflow provides a generated video URL and a manifest of inputs and outputs.]

## Skill Version(s):

1.0.15 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
