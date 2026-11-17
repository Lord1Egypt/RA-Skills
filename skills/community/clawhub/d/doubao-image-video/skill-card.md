## Description:

Doubao Image Video helps agents generate Doubao images and videos, query asynchronous video tasks, wait for completion, and download completed videos through Volcengine Ark.

This skill is ready for commercial/non-commercial use.

## Publisher:

[156554395](https://clawhub.ai/user/156554395)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to create Doubao images and videos, work with reference image URLs, monitor asynchronous video task IDs, and retrieve finished video files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media prompts, image URLs, and task metadata are sent to Volcengine Ark using the user's DOUBAO_API_KEY.

Mitigation: Use the skill only when that third-party transfer is acceptable, and avoid private image URLs or sensitive prompts unless they are approved for Volcengine Ark.

Risk: The optional --download-to path may replace an existing file.

Mitigation: Choose a new, non-sensitive output filename when downloading completed videos.

## Reference(s):

- [API Notes](references/api-notes.md)
- [ClawHub Skill Page](https://clawhub.ai/156554395/skills/doubao-image-video)
- [Volcengine Ark Image Generation Endpoint](https://ark.cn-beijing.volces.com/api/v3/images/generations)
- [Volcengine Ark Video Generation Tasks Endpoint](https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks)

## Skill Output:

**Output Type(s):** [shell commands, configuration, text, JSON, files, guidance]

**Output Format:** [Markdown guidance with shell commands; helper commands emit JSON and can download video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and DOUBAO_API_KEY; optional endpoint and model environment variables configure defaults.]

## Skill Version(s):

0.3.1 (source: server evidence release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
