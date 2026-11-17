## Description:

Handles Discord task-center forum: create task posts, archive tasks by tag, and respect model tags for conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nannyu](https://clawhub.ai/user/nannyu)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to manage Discord forum threads as task-center items, including creating task posts, archiving current tasks, and preserving task state through forum tags. It is intended for OpenClaw workspaces with Discord forum task-center integration enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured Discord bot may create forum threads, edit thread tags, archive tasks, and create a task-center forum channel when requested.

Mitigation: Install only in Discord workspaces where those actions are acceptable, and grant the bot only the Discord permissions needed for the intended task-center workflow.

Risk: If the Discord tool does not support forum thread applied_tags, task status, archive, or model tags may be incomplete.

Mitigation: Confirm forum-tag support before operational use, or require users and administrators to apply missing tags manually in Discord.

Risk: The examples and trigger phrases are primarily Chinese, which can make intended behavior less clear for non-Chinese users.

Mitigation: Localize trigger phrases and operator-facing examples before deploying to teams that do not read Chinese.

## Reference(s):

- [Discord Task Center ClawHub page](https://clawhub.ai/nannyu/skills/discord-task-center)
- [Discord Task Center API and implementation reference](artifact/reference.md)
- [ClawHub Discord skill](https://clawhub.ai/steipete/discord)

## Skill Output:

**Output Type(s):** [Text, Guidance, API Calls, Shell Commands, Configuration]

**Output Format:** [Markdown and plain text replies with Discord tool or API action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured Discord forum task center and compatible Discord tool support for forum threads and tags.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and artifact/clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
