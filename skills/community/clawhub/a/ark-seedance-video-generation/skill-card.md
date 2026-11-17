## Description:

Ark Seedance Video guides agents through Volcengine Ark Seedance video generation with a bundled Node.js runner for task creation, polling, task management, downloads, and artifact handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iunclear](https://clawhub.ai/user/iunclear)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and tool-using agents use this skill to generate and manage Seedance text-to-video and media-conditioned video tasks through Volcengine Ark, including model selection, API authentication, polling, verification, and asset download.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runner can use override flags or environment variables for API keys and base URLs, which can expose credentials or route requests to an unintended endpoint.

Mitigation: Provide ARK_API_KEY through a secure environment mechanism, use the documented Ark endpoint, and avoid --api-key, --base-url, or ARK_BASE_URL unless reviewed.

Risk: Downloading from task JSON or generated URLs can place untrusted or sensitive media artifacts in the workspace.

Mitigation: Use task.json files only from trusted runs, store outputs in workspace-local directories, and treat prompts, task files, generated videos, and downloads as sensitive.

Risk: Local image, video, or audio inputs are uploaded to Volcengine Ark for generation.

Mitigation: Disclose the upload before execution and stop if the operator does not consent.

## Reference(s):

- [Ark Video API Notes](references/ark-video-api.md)
- [Payload Patterns](references/payload-patterns.md)
- [Video Models](references/video-models.md)
- [Video Models JSON](references/video-models.json)
- [Ark auth and base URL](https://www.volcengine.com/docs/82379/1399008)
- [Create video task](https://www.volcengine.com/docs/82379/1520757)
- [Get video task](https://www.volcengine.com/docs/82379/1521309)
- [List video tasks](https://www.volcengine.com/docs/82379/1521675)
- [Delete video task](https://www.volcengine.com/docs/82379/1521720)
- [LAS Seedance supported model list](https://www.volcengine.com/docs/6492/2165104)
- [ClawHub skill page](https://clawhub.ai/iunclear/skills/ark-seedance-video-generation)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, JSON, Generated media assets, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON request and task files, and downloaded video or last-frame assets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and ARK_API_KEY; generated video and last-frame URLs should be downloaded promptly.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
