## Description: <br>
Cost Optimizer helps OpenClaw and Claude Code users reduce token spend with model-routing recommendations, context compression, heartbeat tuning, usage reports, and configuration generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fullstackcrew-alpha](https://clawhub.ai/user/fullstackcrew-alpha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to analyze AI development-tool spending, choose lower-cost models for routine work, compress large contexts, tune heartbeat behavior, and generate cost-aware configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist conversation-derived data and inspect historical or local usage settings. <br>
Mitigation: Review snapshot and report contents, redact sensitive information, choose storage paths deliberately, and keep generated files out of source control when they contain private context. <br>
Risk: Generated configuration changes can alter model routing, heartbeat behavior, budgets, logs, and local settings. <br>
Mitigation: Review proposed diffs before applying them, confirm backups are created, and start with conservative or balanced presets when quality or reliability is more important than maximum savings. <br>


## Reference(s): <br>
- [Cost Optimizer on ClawHub](https://clawhub.ai/fullstackcrew-alpha/cost-optimizer) <br>
- [Model Pricing Reference](references/model-pricing.md) <br>
- [Model Routing Rules](references/routing-rules.md) <br>
- [OpenClaw](https://openclaw.dev) <br>
- [Node.js](https://nodejs.org) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports and recommendations with inline shell commands, JSON configuration snippets, diffs, and optional generated files such as openclaw.json or context snapshots] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or write local configuration, logs, usage reports, and context snapshots when the user confirms the relevant workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact metadata reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
