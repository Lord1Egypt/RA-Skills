## Description:

Collect structured metadata for one YouTube video by video ID, such as title, channel, counts, and details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit Dataify Builder jobs for YouTube video basic metadata by video ID and receive collected JSON results after task monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends YouTube video IDs and a Dataify API TOKEN to Dataify, and use may create paid collection jobs.

Mitigation: Configure DATAIFY_API_TOKEN outside chat, never print or paste real tokens, and confirm user intent when scope or cost could materially increase.

Risk: Server security evidence says the skill is broader and riskier than advertised, with unresolved credential-handling and dependency issues.

Mitigation: Review before installing, keep the advertised scope narrow, disclose batch and subtitle behavior, and resolve credential-handling and dependency concerns before broad deployment.

Risk: The artifact relies on a task-runtime dependency for asynchronous task completion.

Mitigation: Declare or vendor the task-runtime dependency so users can execute monitoring behavior reliably.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dataify-server/skills/dataify-youtube-product-by-id)
- [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill)
- [Dataify API Token Login](https://dashboard.dataify.com/login?utm_source=skill)
- [Dataify Builder Endpoint](https://scraperapi.dataify.com/builder?platform=1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, JSON]

**Output Format:** [Markdown guidance and command examples, with JSON task summaries and collected results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The default deliverable is the final collected result; timed-out monitoring should return the task ID and a resume command without resubmitting the paid task.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
