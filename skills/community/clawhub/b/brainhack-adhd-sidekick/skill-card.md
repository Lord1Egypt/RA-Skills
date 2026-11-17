## Description:

A fully configured OpenClaw agent pack for ADHD-oriented planning, focus support, emotional first aid, routines, study help, life admin, and conversational check-ins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mttbond-byte](https://clawhub.ai/user/mttbond-byte)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill as an ADHD-oriented sidekick that routes conversational requests into task chunking, planning, body doubling, emotional regulation, routines, social scripting, studying, and daily reflection. It is support and planning software, not medical care or crisis support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can build persistent local memory about ADHD traits, medication status, mood, routines, emotional triggers, and productivity patterns.

Mitigation: Before use, confirm where USER.md, MEMORY.md, and memory logs are stored, whether they can be reviewed and deleted, and whether they are synced or backed up.

Risk: The skill can send scheduled Telegram or WhatsApp messages and check-ins without clear consent or retention controls.

Mitigation: Enable proactive messages only with explicit opt-in, clear schedule settings, and a simple way to pause or disable reminders.

Risk: The skill is mental-health-adjacent and includes emotional regulation and meltdown support.

Mitigation: Treat it as support and planning software, not medical care or crisis support, and use professional or emergency support channels when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mttbond-byte/skills/brainhack-adhd-sidekick)
- [ADHD Research Base](artifact/knowledge/adhd-research-base.md)
- [CBT/DBT Toolkit](artifact/knowledge/cbt-dbt-toolkit.md)
- [Tool Integrations Guide](artifact/knowledge/tool-integrations.md)
- [Memory and State Tracking](artifact/MEMORY.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown conversational responses, checklists, schedules, message drafts, and memory-update guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce scheduled check-in prompts and persistent memory entries when the agent environment is configured for them.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
