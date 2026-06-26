## Description: <br>
Create portable OpenClaw cron health checks with deterministic scripts, config, validation, and reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[glucksberg](https://clawhub.ai/user/glucksberg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to build an instance-local OpenClaw cron health kit that audits scheduled jobs, system crons, logs, scheduler metadata, registry notes, and callback notes. It is intended for deterministic report generation and setup guidance rather than general host hardening or broad observability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured cron files, scheduler metadata, registry notes, callback notes, and logs can contain sensitive operational data. <br>
Mitigation: Review configured paths before use, keep reports summarized, and confirm redaction before delivering reports to a chat or topic. <br>
Risk: The optional project validation_command path has a cfg scoping bug in the reviewed release. <br>
Mitigation: Fix the scoping issue or avoid optional validation_command entries before relying on that project validation path. <br>
Risk: Unsafe command probes could expand the skill beyond its intended local diagnostic scope. <br>
Mitigation: Use only the fixed argv probes documented by the skill and reject shell syntax, privilege tools, network clients, absolute command paths, and arbitrary project commands. <br>


## Reference(s): <br>
- [Skill source](artifact/SKILL.md) <br>
- [Setup manual](artifact/references/setup-manual.md) <br>
- [Report format](artifact/references/report-format.md) <br>
- [Porting checklist](artifact/references/porting-checklist.md) <br>
- [Cron health config template](artifact/templates/cron-health-config.json) <br>
- [ClawHub release page](https://clawhub.ai/glucksberg/cron-health-cron) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python script, JSON configuration, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces an instance-local health-check kit and a concise delivery-ready cron health report; routine checks are designed to avoid network access and writes.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
