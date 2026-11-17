## Description:

Download or collect a YouTube audio file from a known video URL. Do not use for video files, metadata, comments, transcripts, or video discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit Dataify collection jobs for YouTube audio URLs, monitor the asynchronous task, and return the collected result. It is intended for audio collection from known YouTube video URLs, not discovery or transcript workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a saved DATAIFY_API_TOKEN and depends on the required dataify-task-operations runtime in the same environment.

Mitigation: Install only when Dataify and the task runtime are trusted, store the API TOKEN in an environment variable or secret manager, and never paste tokens into chat.

Risk: Submitting Dataify jobs may consume account credits.

Mitigation: Confirm each submission and review scope before execution, especially for multiple URLs or media downloads.

Risk: Subtitle options are available even though the skill excludes transcript-focused use cases.

Mitigation: Leave subtitle options disabled unless subtitle collection is explicitly intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-youtube-audio-by-url)
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill)
- [Dataify login](https://dashboard.dataify.com/login?utm_source=skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON task/result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return a task_id, status, submitted parameters, and a summarized final collection result; raw result access should be preserved when payloads are large.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
