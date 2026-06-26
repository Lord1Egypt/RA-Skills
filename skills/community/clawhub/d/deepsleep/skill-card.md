## Description: <br>
Two-phase daily memory persistence for AI agents. v3.0: unified pack+dispatch cron, smart silence handling, memory importance tiers, cross-group correlation, OQ health tracking, and schedule priority system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffchang2024](https://clawhub.ai/user/jeffchang2024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams using OpenClaw use DeepSleep to persist cross-session group memory, generate daily summaries and reminders, and restore recent context before an agent replies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad cross-chat visibility can expose more conversation history than participants expect. <br>
Mitigation: Use the skill only in workspaces where participants have agreed to cross-chat summarization, and avoid all-session visibility unless it is required. <br>
Risk: Stored daily summaries and group snapshots may retain sensitive context longer than intended. <br>
Mitigation: Exclude direct messages and sensitive groups by default, and define retention and deletion rules before enabling the skill. <br>
Risk: Proactive briefs or memory mentions can reveal prior context without clear consent. <br>
Mitigation: Require explicit user action before sending any brief or mentioning prior memory in a chat. <br>


## Reference(s): <br>
- [DeepSleep on ClawHub](https://clawhub.ai/jeffchang2024/deepsleep) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [DeepSleep design notes](references/design.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and configuration file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces daily summaries, per-group memory snapshots, schedule entries, dispatch logs, and setup guidance for OpenClaw agents.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
