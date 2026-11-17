## Description:

Collect YouTube channel or profile records by channel URL or keyword, excluding videos, comments, transcripts, and media downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit Dataify Builder jobs that collect YouTube channel/profile records by channel URL or keyword, then monitor the returned task and retrieve final JSON results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill loads an unpinned external Python helper from dataify-task-operations/scripts and passes the Dataify API token to it.

Mitigation: Review and trust the Dataify runtime dependency before installation or execution, and keep the helper source/version controlled in the deployment environment.

Risk: Profile collection jobs may consume Dataify credits and require an API token.

Mitigation: Configure DATAIFY_API_TOKEN through the environment rather than chat, and use explicit invocation or no-wait behavior for tasks with potentially large scope.

## Reference(s):

- [Modes and Parameters](references/modes-and-parameters.md)
- [Dataify YouTube Profiles on ClawHub](https://clawhub.ai/dataify-server/skills/dataify-youtube-profiles)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON task/result payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns final collected JSON results by default; can stop after submission when explicitly requested.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
