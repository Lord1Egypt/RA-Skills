## Description:

Filters Feishu group-chat messages with a configurable keyword whitelist so the bot only replies when a message contains an allowed keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnhejunlin](https://clawhub.ai/user/johnhejunlin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators maintaining Feishu group bots use this skill to gate replies on a local keyword whitelist, reducing unrelated replies and token use in busy group chats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An empty whitelist causes the bot to reply without filtering.

Mitigation: Keep at least one intended trigger keyword in config/whitelist.txt unless unfiltered replies are deliberate.

Risk: Broad or ambiguous keywords can trigger replies in unrelated group messages.

Mitigation: Use specific keywords and review the whitelist before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnhejunlin/skills/feishu-message-group-whitelist)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown instructions and plain-text whitelist configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses one keyword per line; an empty whitelist intentionally disables filtering.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
