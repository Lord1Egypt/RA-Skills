## Description: <br>
Use when updating OpenClaw or debugging an OpenClaw instance after an update. This skill acts as a structured update runbook with emphasis on gateway startup, service-manager state, plugin registry and install drift, bundled-vs-npm/clawhub plugin confusion, stale config carried across upgrades, channel health, task ledger corruption, and logs that explain why the updated system is slow, disconnected, or half-broken. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bkf-gitty](https://clawhub.ai/user/bkf-gitty) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Operators and engineers maintaining OpenClaw hosts use this skill to audit updates, diagnose post-upgrade failures, and verify service, plugin, config, channel, task, and model-route health before making the smallest necessary repair. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides broad update, restart, plugin-change, and secret-handling guidance that could change an OpenClaw host if followed without review. <br>
Mitigation: Review each proposed command before execution and prefer the smallest repair that makes host state consistent. <br>
Risk: Diagnostics may encounter tokens, service environment files, secret-bearing backups, or other sensitive credentials. <br>
Mitigation: Avoid printing or pasting tokens, protect or delete secret-bearing backups, and prefer platform secret-management commands when available. <br>


## Reference(s): <br>
- [Failure Patterns](references/failure-patterns.md) <br>
- [ClawHub skill page](https://clawhub.ai/bkf-gitty/claw-update-runbook) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with command examples and operator checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces diagnostic and repair guidance for review before execution.] <br>

## Skill Version(s): <br>
1.0.6 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
