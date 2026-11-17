## Description:

Generates a daily morning brief with Shanghai weather and the top five V2EX hot topics, then sends the brief through Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alibaba4184hub](https://clawhub.ai/user/alibaba4184hub)

### License/Terms of Use:

MIT-0

## Use Case:

Users and automation agents use this skill to receive a scheduled or manually triggered daily brief covering Shanghai weather and current V2EX hot topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts wttr.in and v2ex.com and sends the resulting brief through Telegram.

Mitigation: Confirm those external services and the Telegram destination are acceptable before installation.

Risk: A cron trigger can send unattended daily messages.

Mitigation: Enable the scheduled trigger only when unattended delivery is intended, and review the schedule and recipient before deployment.

Risk: Telegram credential or chat configuration mistakes can send the brief to the wrong destination.

Mitigation: Configure Telegram credentials carefully and restrict the bot to the intended chat or channel.

## Reference(s):

- [wttr.in Shanghai weather endpoint](https://wttr.in/Shanghai?format=3)
- [V2EX hot topics API](https://www.v2ex.com/api/topics/hot.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown-style daily brief with date, weather, and ranked topic entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes the current date, one wttr.in weather string, and five V2EX hot-topic title and node pairs.]

## Skill Version(s):

1.0.2 (source: server release evidence, released 2026-03-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
