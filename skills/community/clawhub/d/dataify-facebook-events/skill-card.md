## Description:

Collect Facebook events from an event-list URL, event-search URL, or event URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit Dataify Builder jobs that collect Facebook event data from event list URLs, event search URLs, or specific event URLs, then monitor the task and return the collected result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Facebook event URLs and task parameters to Dataify and requires a Dataify API token.

Mitigation: Use it only when sharing those inputs with Dataify is acceptable, configure DATAIFY_API_TOKEN outside chat, and never paste the token into conversation.

Risk: The security review notes an unaudited sibling runtime that receives the API token.

Mitigation: Review before installing and require the publisher to package or pin the task runtime before treating the release as low risk.

Risk: Localized token-handling instructions are inconsistent.

Mitigation: Follow the server security guidance and confirm token handling behavior before deployment.

## Reference(s):

- [Modes and Parameters](references/modes-and-parameters.md)
- [ClawHub Skill Page](https://clawhub.ai/dataify-server/skills/dataify-facebook-events)
- [Dataify Dashboard Login](https://dashboard.dataify.com/login?utm_source=skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON task/result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit paid Dataify Builder tasks, monitor asynchronous task status, and return final JSON results or a resumable task ID.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
