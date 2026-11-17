## Description:

Generates AI videos through the Baiyin Open Platform, including text-to-video, image-to-video, and task status queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiuping520](https://clawhub.ai/user/jiuping520)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure Baiyin video generation jobs, provide prompts or media inputs, submit jobs, and track completion until a video URL or failure message is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local media paths to an external Baiyin service.

Mitigation: Use a dedicated Baiyin API key, provide only intended media files, and confirm uploads before sending local files.

Risk: Prompts and media are sent to ai.hikoon.com for video generation.

Mitigation: Avoid submitting confidential prompts, private files, or sensitive media unless the service is approved for that data.

Risk: The skill asks agents to perform automatic self-update checks before normal operation.

Mitigation: Review updates before installation and scan the skill package before deployment.

## Reference(s):

- [API Schema](references/api-schema.md)
- [Interaction Rules](references/interaction-rules.md)
- [Error and Polling](references/error-and-polling.md)
- [Example Flow](references/example-flow.md)
- [ClawHub Skill Page](https://clawhub.ai/jiuping520/skills/baiyin-video-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [User-facing text or Markdown with shell command execution by the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return task identifiers, request identifiers, status updates, error messages, and generated video URLs.]

## Skill Version(s):

1.0.3 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
