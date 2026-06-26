## Description: <br>
Lightweight operational audit logging for AI assistants, agent workspaces, and personal automation systems that need structured records of high-value actions, risk levels, summaries, and open follow-up items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lethehades](https://clawhub.ai/user/lethehades) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, AI assistant operators, and agent workspace maintainers use this skill to create a lightweight audit trail for installs, configuration changes, repository operations, publishing flows, secret-related events, export-safety checks, and follow-up risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The initialization script can truncate the current day's JSONL audit log if it is run again. <br>
Mitigation: Review or patch scripts/init_audit.sh before installation so it creates the daily JSONL file only when missing. <br>
Risk: Audit logs can contain sensitive operational context if users record secrets or publish local logs. <br>
Mitigation: Keep audit logs private, exclude them from public exports, and record only metadata for secret-related events. <br>


## Reference(s): <br>
- [Agent Audit Log on ClawHub](https://clawhub.ai/lethehades/agent-audit-log) <br>
- [Schema Reference](references/schema.md) <br>
- [Risk Model](references/risk-model.md) <br>
- [Export Safety](references/export-safety.md) <br>
- [Open Items](references/open-items.md) <br>
- [Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, JSON, JSONL, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON/JSONL schemas, examples, and shell command usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports local audit files such as daily JSONL logs, JSON indexes, open-item trackers, and human-readable Markdown summaries.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
