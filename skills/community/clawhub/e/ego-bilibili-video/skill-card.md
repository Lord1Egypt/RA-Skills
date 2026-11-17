## Description:

Publish local videos to Bilibili through Ego Lite, with a login check and an explicit --yes required before submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terryso](https://clawhub.ai/user/terryso)

### License/Terms of Use:

MIT-0

## Use Case:

Video creators use this skill to submit a local video to Bilibili's creator platform. It checks login status, prepares the title, description, tags, partition, and optional separate cover images, then reports the submission status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the release suspicious with medium confidence, and only 45% of the artifact was fully inspected.

Mitigation: Review the complete artifact and wait for a more complete inspection and resolution of the publishing success check before installing or running the skill.

Risk: A run with --yes submits the video to Bilibili; approved submissions become public.

Mitigation: Check the target account, video, covers, and submission details, and use --yes only when you intend to submit.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/terryso/skills/ego-bilibili-video)
- [Bilibili creator upload page](https://member.bilibili.com/platform/upload/video/frame)
- [Login guidance](artifact/references/login.md)
- [Input requirements](artifact/references/inputs.md)
- [Publishing pitfalls](artifact/references/pitfalls.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Text]

**Output Format:** [JSON status results and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A successful submission may include a BV URL; if the identity cannot be confirmed, the result reports that status.]

## Skill Version(s):

0.1.0 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
