## Description:

Manages Discord task-center forums by creating and archiving task posts with tags, respecting model tags, and optionally creating a six-ministries channel structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nannyu](https://clawhub.ai/user/nannyu)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to manage Discord task-center forums as one-task-per-thread workflows, including task creation, task archival, model-tag awareness, and optional Discord channel setup from bundled templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a separately installed Discord integration that may receive meaningful bot permissions.

Mitigation: Review and preferably pin the @steipete/discord dependency, then configure the Discord bot with least-privilege permissions.

Risk: The skill can create forum threads, edit thread tags, and, when explicitly requested, create channel and category structures in a Discord server.

Mitigation: Limit MANAGE_CHANNELS and MANAGE_THREADS access to trusted bot deployments and review channel-creation requests before execution.

## Reference(s):

- [Discord Dynasty ClawHub page](https://clawhub.ai/nannyu/skills/discord-dynasty)
- [Discord task-center API reference](reference.md)
- [Six-ministries full template](templates/six-ministries.json)
- [Six-ministries minimal template](templates/six-ministries-minimal.json)
- [Discord integration skill](https://clawhub.ai/steipete/discord)
- [OpenClaw Discord channel docs](https://docs.openclaw.ai/channels/discord)
- [Ai Court architecture inspiration](https://clawhub.ai/wanikua/ai-court)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with Discord tool-call guidance and JSON channel-template configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in Discord forum threads, thread tag edits, or channel and category creation when the configured Discord integration executes requested actions.]

## Skill Version(s):

1.2.0 (source: evidence.release.version and artifact/clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
