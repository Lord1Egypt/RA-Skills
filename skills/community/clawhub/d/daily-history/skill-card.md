## Description:

Today in history -- 3-5 major events on this date with context and lasting impact, presented as a bilingual English/Chinese timeline card with daily morning push support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiajiaoy](https://clawhub.ai/user/jiajiaoy)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to generate concise daily history timeline content in English and Chinese, including notable events, context, and lasting impact. Users may also configure recurring morning and evening push messages for supported channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can configure persistent scheduled push jobs and recurring outbound messages.

Mitigation: Confirm the destination channel, recipient user ID, schedule, timezone, and disable path before enabling push jobs; avoid environments where skill output can create cron tasks without explicit authorization.

## Reference(s):

- [Daily History ClawHub Skill Page](https://clawhub.ai/jiajiaoy/skills/daily-history)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Bilingual markdown guidance and generated single-file HTML timeline output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit scheduler control commands for recurring push messages when push management is used.]

## Skill Version(s):

1.0.2 (source: server release evidence, released 2026-04-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
