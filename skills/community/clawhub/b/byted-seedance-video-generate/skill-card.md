## Description:

Generate videos using Seedance models from text prompts, images, videos, audio, or other reference materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create Seedance videos from text, image, video, and audio inputs, then return generated video URLs and task status details to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed if an agent writes them into workspace files or sends them to an unintended configurable endpoint.

Mitigation: Preconfigure API keys through a secure secret mechanism, avoid workspace credential files, and verify ARK_BASE_URL or MODEL_VIDEO_API_BASE before use.

Risk: Prompts, signed media URLs, and private reference assets are sent to the configured video service.

Mitigation: Do not submit confidential prompts, signed URLs, or private assets unless the configured provider, account controls, and data handling are trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-seedance-video-generate)
- [Publisher profile](https://clawhub.ai/user/volcengine-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, API calls]

**Output Format:** [Markdown with video embeds, JSON task results, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns generated video URLs, local file path guidance when available, task IDs for pending jobs, and error details for failed jobs.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
