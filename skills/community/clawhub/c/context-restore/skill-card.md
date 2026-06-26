## Description: <br>
Context Restore restores saved OpenClaw conversation context by reading compressed context files and generating structured status reports with projects, tasks, operations, and timelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexunitario-sketch](https://clawhub.ai/user/alexunitario-sketch) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to resume work after a new or interrupted session by restoring recent project state, pending tasks, operations, and timeline summaries from saved context files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads saved conversation context and local project status files, which may include sensitive work history or project details. <br>
Mitigation: Install only where those local files are intended to be read, and review configured paths before running the skill. <br>
Risk: Optional auto mode and cron monitoring can repeatedly inspect context files in the background. <br>
Mitigation: Enable background monitoring only after reviewing the exact cron command, interval, log destination, and files being monitored. <br>
Risk: Notification examples and integrations may send restored context through Telegram, email, or another outbound channel. <br>
Mitigation: Treat outbound notifications as separate integrations that require explicit consent, destination review, and careful secret handling. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/alexunitario-sketch/context-restore) <br>
- [README](artifact/README.md) <br>
- [Usage Guide](artifact/docs/USAGE.md) <br>
- [API Reference](artifact/docs/API.md) <br>
- [Design Decisions](artifact/references/design.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text reports, optional JSON summaries, and CLI guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports minimal, normal, and detailed report levels; optional timeline, filtering, diff, confirmation, Telegram chunking, and auto-monitoring modes.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
