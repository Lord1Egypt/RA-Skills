## Description: <br>
Fractal Memory helps an agent organize persistent workspace memory through daily, weekly, monthly, and core rollups to reduce context overflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bugmaker2](https://clawhub.ai/user/bugmaker2) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to set up hierarchical memory files, scheduled rollups, and migration guidance for long-running agents that need concise persistent context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently stores chat-derived memory in workspace files, which may capture sensitive personal, business, or secret material. <br>
Mitigation: Avoid storing secrets or sensitive personal data, review generated memory files regularly, and keep a clear deletion and backup process. <br>
Risk: Scheduled rollups can modify memory files in the background after installation. <br>
Mitigation: Review cron configuration before enabling it, keep rollup jobs disabled until tested, and maintain a documented way to disable the jobs. <br>
Risk: Daily diary content may be sent to the configured OpenClaw LLM backend during rollup processing. <br>
Mitigation: Use the skill only with an approved LLM configuration, disable LLM rollup or switch to local-only processing when required, and review backend data-handling expectations. <br>


## Reference(s): <br>
- [Architecture](references/architecture.md) <br>
- [Cron Setup Guide](references/cron-setup.md) <br>
- [Migration Guide](references/migration-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python scripts, and JSON configuration templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces file- and schedule-oriented guidance for memory setup, migration, rollups, and integrity checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
