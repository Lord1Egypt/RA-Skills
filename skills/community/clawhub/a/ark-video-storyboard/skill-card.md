## Description:

Generate a storyboard and prompts from a scene or reference images, confirm the script with the user, then optionally submit multi-segment video generation tasks to the Volcengine Ark video API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yunni123](https://clawhub.ai/user/yunni123)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and video creators use this skill to turn a scene idea or reference images into a structured storyboard, segment plan, and generation prompts. After explicit approval, it can submit segments to the Volcengine Ark video API, poll for results, and download generated media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ark API credentials, prompts, and reference images may be used with an external video generation service.

Mitigation: Use a limited Ark API key and avoid sensitive prompts or reference images.

Risk: Generated videos are downloaded and stored locally, and the workflow can send media externally.

Mitigation: Confirm where files will be saved and sent, and do not send media to Feishu unless the destination is explicit.

Risk: The skill defaults unspecified human characters to East Asian appearance.

Mitigation: Remove or override the default and ask the user for character attributes when they matter.

Risk: The security summary reports weak safeguards around API, downloader, and media-sending behavior.

Mitigation: Review and harden the API and downloader scripts before using the skill in a shared or monitored environment.

## Reference(s):

- [Ark Video API Notes](references/api.md)
- [Storyboard Schema](references/storyboard-schema.md)
- [Prompt Rules](references/prompt-rules.md)
- [Examples](references/examples.md)
- [Volcengine Ark video generation tasks endpoint](https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks)
- [Volcengine Ark task status endpoint](https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/{id})

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration instructions, Files, Guidance]

**Output Format:** [Markdown storyboard and prompt guidance, JSON storyboard and API result data, shell commands, and optional local MP4 files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can call the Volcengine Ark API, poll tasks, and download generated videos after explicit user approval.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
