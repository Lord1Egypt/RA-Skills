## Description: <br>
Computer Efficiency Skill helps an agent inspect macOS, Windows, and Linux system health, score performance, suggest cleanup, identify memory-heavy processes, and prepare scheduled health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[perrykono-debug](https://clawhub.ai/user/perrykono-debug) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, technical users, and support agents use this skill to generate cross-platform system health reports, review optimization suggestions, and plan confirmed cleanup or process-management actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cleanup guidance could delete useful files or logs if executed without review. <br>
Mitigation: Require a clear list of items, estimated space, risk level, backup location, and explicit confirmation before any cleanup. <br>
Risk: Process-management guidance could interrupt user applications or system services. <br>
Mitigation: Show memory-heavy processes first, distinguish user applications from system processes, and require explicit confirmation before terminating any process. <br>
Risk: Scheduled health checks could create recurring actions the user did not intend. <br>
Mitigation: Confirm the schedule, check contents, and alert thresholds before creating or changing recurring checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/perrykono-debug/computer-efficiency-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with inline shell commands, PowerShell commands, tables, and JSON schedule examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before cleanup, file deletion, process termination, or system configuration changes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
