## Description:

Generate visual HTML summaries from OpenClaw session history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[monaxamo](https://clawhub.ai/user/monaxamo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to summarize chat, planning, or decision sessions into shareable visual artifacts and companion summary files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad authority and may write outside the intended output folder if output slugs or locations are influenced by untrusted content.

Mitigation: Use trusted or manually reviewed output slugs and directories, and review generated paths before opening or sharing artifacts.

Risk: Conversation history can contain sensitive chats or private identifiers.

Mitigation: Use it only for sessions that are appropriate to summarize, and manually redact sensitive chats before running the skill.

Risk: Generated local HTML may be unsafe if renderer output is not reviewed.

Mitigation: Review generated HTML before broad use and apply the publisher guidance to harden renderer paths and HTML validation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/monaxamo/skills/conversation-visualizer)
- [Project homepage](https://github.com/openclaw/skills/conversation-visualizer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files]

**Output Format:** [Markdown status text with generated self-contained HTML, PNG, Markdown, and PowerPoint artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local session history and local model inference; generated HTML is self-contained.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
