## Description:

Generate images and media using fal.ai API (Flux, Gemini image, etc.). Use when asked to generate images, run AI image models, create visuals, or anything involving fal.ai. Handles queue-based requests with automatic polling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxela](https://clawhub.ai/user/sxela)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to submit, poll, and retrieve fal.ai image, image-editing, and video-to-video generation jobs from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, images, and videos are sent to fal.ai for generation.

Mitigation: Avoid submitting confidential or sensitive media unless the deployment owner has approved fal.ai use for that data.

Risk: Full request contents may remain in the local pending-request file.

Mitigation: Regularly inspect or delete ~/.openclaw/workspace/fal-pending.json, especially after jobs involving private prompts or media.

Risk: API keys can be read from local configuration files.

Mitigation: Prefer FAL_KEY in a protected environment variable and limit access to local OpenClaw configuration files.

## Reference(s):

- [Model schemas](artifact/references/models.json)
- [fal.ai API keys](https://fal.ai/dashboard/keys)
- [ClawHub skill page](https://clawhub.ai/sxela/skills/falai)
- [Publisher profile](https://clawhub.ai/user/sxela)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with Python and shell snippets; CLI and API operations return JSON, media URLs, or data URI strings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Submits queue-based fal.ai jobs, polls pending requests, and can persist request metadata locally for later retrieval.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
