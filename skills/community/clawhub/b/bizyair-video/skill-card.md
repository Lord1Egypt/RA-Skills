## Description:

BizyAir Video helps an agent create asynchronous BizyAir video-generation tasks from a source image or first and last frames, choose among five documented workflows, and return task IDs plus result links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bozoyan](https://clawhub.ai/user/bozoyan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit image-to-video and first/last-frame video tasks to BizyAir, then query asynchronous results. It is useful when an agent needs to produce shell commands, API payloads, task IDs, and Markdown result tables for generated videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and image or frame URLs are sent to api.bizyair.cn under the user's BIZYAIR_API_KEY.

Mitigation: Use only intended BizyAir accounts, avoid sensitive media or prompts, and confirm data-sharing expectations before running the skill.

Risk: The package bundles image-angle scripts that are under-disclosed relative to the video-generation description.

Mitigation: Review or remove create_angle_task.sh and get_task_outputs.sh before deployment if image-angle workflows are not needed.

Risk: Broad or arbitrary BizyAir workflow IDs can call unintended workflows or consume API quota.

Mitigation: Restrict execution to reviewed workflow IDs and trusted JSON parameters unless a trusted operator approves an additional workflow.

Risk: Shell scripts accept URLs, prompts, and JSON parameters that may come from users.

Mitigation: Do not pass untrusted JSON, URLs, or prompts through the scripts without proper escaping and validation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bozoyan/skills/bizyair-video)
- [BizyAir create task endpoint](https://api.bizyair.cn/w/v1/webapp/task/openapi/create)
- [BizyAir outputs endpoint](https://api.bizyair.cn/w/v1/webapp/task/openapi/outputs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with shell commands, JSON request bodies, asynchronous task IDs, and result tables containing generated media links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BIZYAIR_API_KEY and sends prompts plus image or frame URLs to BizyAir APIs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
