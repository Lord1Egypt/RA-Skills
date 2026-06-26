## Description: <br>
A comprehensive, self-evolving skill designed to diagnose and solve OpenClaw issues by following a structured, multi-stage resolution cycle. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikewongonline](https://clawhub.ai/user/mikewongonline) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to diagnose Gateway, runtime, configuration, API key, and repair issues, then validate fixes with reports, dashboards, and regression comparisons. The optional watchdog monitors Gateway health and sends alerts when configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local repair actions, kill processes, archive session files, run a watchdog, and register autostart. <br>
Mitigation: Treat each repair, watchdog, session archiving, and --install autostart action as a separate opt-in decision with a rollback or uninstall path. <br>
Risk: Diagnostic output can include credentials, logs, or local operational details and may be sent through Feishu or WebChat alerts. <br>
Mitigation: Review and redact diagnostic output before enabling external notifications, and configure alert channels only when intentionally needed. <br>
Risk: Broad auto-repair invocations may change local OpenClaw behavior or hide the root cause of an issue. <br>
Mitigation: Prefer scoped diagnosis first, save a baseline before fixes, review proposed repair scope, and compare results after any repair. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mikewongonline/autofix) <br>
- [Installation guide](INSTALL.md) <br>
- [Master workflow](SKILL.md) <br>
- [v6.1 changelog](docs/reports/CHANGES_v6.1.md) <br>
- [Pre-check module](docs/MODULE_01_PreCheck.md) <br>
- [Search-chain module](docs/MODULE_02_SearchChain.md) <br>
- [Validation and action module](docs/MODULE_03_ValidationAction.md) <br>
- [Finalization module](docs/MODULE_04_Finalization.md) <br>
- [Example usage](docs/tutorials/EXAMPLE_usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, HTML files] <br>
**Output Format:** [Markdown or plain text guidance with shell commands, JSON diagnostic reports, and optional HTML dashboard output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local OpenClaw and Python diagnostic scripts; watchdog deployment and external alerting are optional.] <br>

## Skill Version(s): <br>
6.1.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
