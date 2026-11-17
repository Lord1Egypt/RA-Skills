## Description:

Assists agents with submitting and checking batch image and video generation jobs through a local DYU client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaolou888](https://clawhub.ai/user/xiaolou888)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to turn conversational requests into text-to-image, image-to-image, text-to-video, image-to-video, and batch media-generation tasks. The skill also helps check client readiness, query task status, and return generated result URLs from the local client.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local DYU client may route prompts or reference images through a configured external AI service.

Mitigation: Use the skill only with a trusted local client and avoid submitting confidential prompts or private images unless that external processing is acceptable.

Risk: The executable client can be redirected away from the promised localhost endpoint.

Mitigation: Keep the client endpoint fixed to localhost and do not allow prompts or other skills to change the base URL.

## Reference(s):

- [Video generation interface](artifact/references/video_generate.md)
- [Image generation interface](artifact/references/image_generate.md)
- [Task query interface](artifact/references/task_query.md)
- [ClawHub skill page](https://clawhub.ai/xiaolou888/skills/ai-productivity-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with text code blocks, Python snippets, task IDs, status summaries, and raw result URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Asynchronous generation: successful submissions return task IDs; result URLs should be preserved verbatim, including query parameters.]

## Skill Version(s):

1.0.0 (source: release evidence, SKILL.md frontmatter, artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
