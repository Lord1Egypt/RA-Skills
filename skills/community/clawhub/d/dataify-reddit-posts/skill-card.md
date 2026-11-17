## Description:

Collect Reddit posts by post URL, keyword, or subreddit URL through Dataify Builder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit and monitor Dataify Builder jobs that collect Reddit posts by URL, keyword, or subreddit URL. It is intended to return the final collected JSON result when monitoring completes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that the skill imports unaudited sibling runtime code and passes the Dataify API token to it.

Mitigation: Install only after reviewing or pinning the expected dataify-task-operations runtime, and avoid pasting API tokens into chat.

Risk: Using the Dataify Builder service may consume Dataify credits.

Mitigation: Review the selected collection mode and requested volume before execution, especially for multiple inputs or high-volume jobs.

## Reference(s):

- [Modes and parameters](references/modes-and-parameters.md)
- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-reddit-posts)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON task or result payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return a task_id and resume guidance if asynchronous monitoring times out; otherwise returns the final collected JSON result.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
