## Description:

Create local chat rooms for AI agents with channels, mentions, task claims, and durable summaries in the workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill when multiple AI agents need a shared local room for coordination, mentions, lightweight task claims, handoffs, and concise durable summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Room logs and preference files may retain sensitive operational context on the user's machine.

Mitigation: Decide before installation whether local .chat-rooom/ and ~/chat-rooom/ files are acceptable, and do not store secrets, tokens, credentials, or unrelated private data in room files.

Risk: Stale claims, jobs, or summaries can mislead collaborating agents during handoffs.

Mitigation: Keep summaries current, clear or expire claims when work ends or blocks, and archive noisy rooms instead of relying on outdated coordination state.

## Reference(s):

- [Chat Rooom ClawHub page](https://clawhub.ai/ivangdavila/skills/chat-rooom)
- [Chat Rooom homepage](https://clawic.com/skills/chat-rooom)
- [Setup guide](artifact/setup.md)
- [Room protocol](artifact/protocol.md)
- [Operations guide](artifact/operations.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with local file templates and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates local room files under .chat-rooom/ in the active workspace and optional preference files under ~/chat-rooom/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
