## Description:

Publish a caller-provided local video to the Douyin creator center with a login check before upload; the skill does not download videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terryso](https://clawhub.ai/user/terryso)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and agents use this skill to publish a supplied local video, title, and description to the Douyin creator center. It checks login status first and gives the user sign-in guidance when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Overlapping publishing runs can mix up videos and captions.

Mitigation: Use private per-run settings; until that is available, serialize publishing in a trusted single-user environment.

Risk: Publishing is public and immediate by default, using the currently logged-in Douyin account.

Mitigation: Confirm the intended account and approve the video, title, and description before publishing.

Risk: Temporary settings or failure screenshots may remain after a run.

Mitigation: Remove leftover settings and failure screenshots after publishing.

## Reference(s):

- [Douyin creator center](https://creator.douyin.com)
- [Input requirements](references/inputs.md)
- [Login guidance](references/login.md)
- [Publishing pitfalls](references/pitfalls.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, JSON]

**Output Format:** [JSON status with concise text or login guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Publishes the supplied video; does not download or create a video file.]

## Skill Version(s):

0.1.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
