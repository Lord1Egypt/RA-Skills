## Description: <br>
Automatically sets up a three-layer OpenClaw memory system with long-term memory, daily notes, and a nightly fact extraction cron job. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[casperzinou](https://clawhub.ai/user/casperzinou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to initialize a local memory workflow that records durable facts, decisions, preferences, and daily notes for future OpenClaw sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The nightly extraction job can retain conversation-derived facts over time without clear consent, deletion, or sensitivity boundaries. <br>
Mitigation: Before enabling the cron job, define retention rules, exclude secrets and sensitive personal data, and document how users can inspect, edit, or remove stored memory files. <br>
Risk: The recurring cron job may run in an unexpected timezone, session context, or storage location. <br>
Mitigation: Confirm the exact cron schedule, timezone, command, working directory, and storage paths before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/casperzinou/ai-memory-system) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with templates and an inline shell command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory file templates and cron setup guidance for an OpenClaw agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
