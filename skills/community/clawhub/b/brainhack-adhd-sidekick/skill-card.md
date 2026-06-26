## Description: <br>
Brainhack — ADHD Sidekick is an OpenClaw agent pack for ADHD support that provides task organization, planning, body doubling, emotional regulation, study help, routines, win tracking, and Telegram or WhatsApp-based interaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mttbond-byte](https://clawhub.ai/user/mttbond-byte) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users use this agent pack as an ADHD-oriented sidekick for organizing messy inputs, breaking tasks into smaller steps, planning days and weeks, running focus sessions, navigating overwhelm, building routines, and recording progress. Developers or operators can configure it in OpenClaw with optional Telegram, WhatsApp, calendar, reminder, and task-app integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores sensitive ADHD profile details, moods, routines, triggers, open tasks, and session summaries. <br>
Mitigation: Configure memory use explicitly, review stored entries regularly, define retention expectations, and avoid recording details the user would not want persisted. <br>
Risk: The skill can send proactive outreach through scheduled messages without enough consent or control details. <br>
Mitigation: Require explicit opt-in for proactive messages, confirm channel and timing preferences, and provide a clear way to pause or stop outreach. <br>
Risk: Telegram, WhatsApp, calendar, reminder, and task-app integrations can expose personal or sensitive context to third-party platforms. <br>
Mitigation: Connect external tools only after confirmation, explain the privacy tradeoff, and use manual formats when the user does not want an integration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mttbond-byte/brainhack-adhd-sidekick) <br>
- [README](artifact/README.md) <br>
- [ADHD Executive Function](artifact/knowledge/adhd-executive-function.md) <br>
- [ADHD Research Base](artifact/knowledge/adhd-research-base.md) <br>
- [CBT/DBT Toolkit](artifact/knowledge/cbt-dbt-toolkit.md) <br>
- [Dopamine Design](artifact/knowledge/dopamine-design.md) <br>
- [Tool Integrations](artifact/knowledge/tool-integrations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown conversational responses, structured task lists, session notes, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update memory files and propose calendar, reminder, or task-app actions when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
