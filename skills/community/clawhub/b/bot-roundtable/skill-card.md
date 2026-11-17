## Description:

Enables multiple bots in a Feishu group to present expert perspectives and hold roundtable-style discussions automatically or on demand.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linbo405](https://clawhub.ai/user/linbo405)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Feishu workspace operators use this skill to coordinate multiple bot personas that analyze, debate, or discuss a topic in a group chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic broad triggers and group-posting behavior can send multi-bot replies in chats where participants did not expect automation.

Mitigation: Enable the skill only in Feishu groups where participants expect automated replies, prefer explicit command-style triggers, and restrict who can invoke it.

Risk: Bot credentials are required for Feishu app accounts and may be mishandled if storage expectations are unclear.

Mitigation: Clarify where credentials are stored before deployment and keep secrets in the intended secure configuration path rather than in public skill files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linbo405/skills/bot-roundtable)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Feishu message drafts and configuration guidance for multi-bot group discussions.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
