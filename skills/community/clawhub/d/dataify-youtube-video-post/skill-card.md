## Description:

Collect YouTube video-post records by URL, search filters, hashtag, podcast URL, keyword, or Explore URL. Use for video discovery or lists. Do not use to download media files or retrieve only one video's metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit Dataify Builder jobs that collect YouTube video-post records from channel video URLs, search filters, hashtags, podcast or playlist URLs, keywords, or Explore URLs, then monitor the task and return the final collected result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends YouTube collection targets and a Dataify bearer token to Dataify.

Mitigation: Use the skill only when the user intends to submit Dataify collection jobs, keep the API TOKEN in the DATAIFY_API_TOKEN environment variable, and never expose the token in chat or logs.

Risk: Implicit or high-volume collection jobs may consume paid Dataify credits.

Mitigation: Confirm consequential scope choices before execution and, after a successful submission, resume or monitor the returned task_id instead of resubmitting interrupted work.

Risk: The helper script depends on task_runtime code located outside this package.

Mitigation: Install and run the skill only with a trusted Dataify task-operations runtime, and review that surrounding runtime before deployment.

## Reference(s):

- [Modes and Parameters](references/modes-and-parameters.md)
- [ClawHub Skill Page](https://clawhub.ai/dataify-server/skills/dataify-youtube-video-post)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance, shell commands, and JSON task/result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DATAIFY_API_TOKEN for execution; submits asynchronous collection jobs and normally returns the final collected JSON result.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
