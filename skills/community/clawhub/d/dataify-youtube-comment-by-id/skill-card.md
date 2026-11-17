## Description:

Collect YouTube comments for a known video ID. Do not use for video metadata, transcripts, media downloads, or keyword discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit Dataify YouTube comment collection jobs by video ID, monitor the returned task, and retrieve final collected results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script loads sibling Dataify task-operations runtime code while passing it the API token.

Mitigation: Review before installing and use only with a trusted local Dataify task-operations runtime.

Risk: Users may expose secrets if they paste an API TOKEN into chat.

Mitigation: Configure DATAIFY_API_TOKEN through the local shell or environment and never print or paste the token in conversation.

Risk: The skill may submit and monitor Dataify jobs by default, which can consume account credits.

Mitigation: Confirm high-volume or multi-input collection scope before execution and resume existing task IDs instead of resubmitting paid jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-youtube-comment-by-id)
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill)
- [Dataify API token login](https://dashboard.dataify.com/login?utm_source=skill)
- [Dataify Builder endpoint](https://scraperapi.dataify.com/builder?platform=1)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON task or result output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May wait for asynchronous Dataify task completion and summarize large JSON payloads while preserving access to raw results.]

## Skill Version(s):

1.3.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
