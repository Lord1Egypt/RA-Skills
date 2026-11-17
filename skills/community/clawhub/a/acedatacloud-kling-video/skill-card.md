## Description:

Guides agents through Kling video and commercial-media generation using AceDataCloud's API, including text and image prompts, storyboards, motion control, talking photos, and lip sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acedatacloud](https://clawhub.ai/user/acedatacloud)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to prepare Kling video-generation requests, configure API access, and follow up on asynchronous media tasks through AceDataCloud.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, media URLs, audio, and callback URLs are sent to AceDataCloud.

Mitigation: Send only inputs you are authorized to share with the service.

Risk: An exposed API key can permit unauthorized requests.

Mitigation: Keep the key in the documented local environment or shell environment, out of prompts and repositories, and restrict allowed APIs where possible.

Risk: Video generation can incur charges, including from repeated requests while a task is still running.

Mitigation: Review current pricing and poll the existing task ID rather than submitting the same request again.

## Reference(s):

- [Kling Video on ClawHub](https://clawhub.ai/acedatacloud/skills/kling)
- [AceDataCloud API key setup](https://github.com/AceDataCloud/Skills/blob/main/skills/_shared/authentication.md)
- [AceDataCloud async task guidance](https://github.com/AceDataCloud/Skills/blob/main/skills/_shared/async-tasks.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Code]

**Output Format:** [Markdown with shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requests may return task IDs requiring follow-up; generated videos are returned by the external service.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
