## Description: <br>
AgentOps helps OpenClaw users check agent health, analyze logs, monitor performance, manage alerts, optimize configuration, coordinate multiple agents, diagnose failures, and generate performance reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keybryant](https://clawhub.ai/user/keybryant) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect and manage OpenClaw agent operations, including local health checks, log review, performance monitoring, alert rules, configuration guidance, coordination analysis, diagnostics, and operational reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local diagnostics and reports may expose paths, host details, process commands, or secrets already present in local logs. <br>
Mitigation: Run the skill as a normal user for OpenClaw-related tasks and review or redact outputs before sharing them. <br>
Risk: The skill inspects local OpenClaw logs, configuration, workspace metadata, process state, and system metrics. <br>
Mitigation: Use it only in intended OpenClaw environments and avoid pointing log or configuration analysis at unrelated sensitive files. <br>


## Reference(s): <br>
- [OpenClaw configuration reference](references/openclaw_config_reference.md) <br>
- [Performance metrics reference](references/metrics_reference.md) <br>
- [Troubleshooting guide](references/troubleshooting.md) <br>
- [AgentOps ClawHub release](https://clawhub.ai/keybryant/agentops) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Plain text, JSON, and Markdown reports, often accompanied by shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some script options can write local JSON alert rules or Markdown report files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
