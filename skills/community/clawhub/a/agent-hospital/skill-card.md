## Description: <br>
AI-powered diagnosis and repair for AI agents. Send your health data, get diagnosed, execute prescribed repairs, report back until healed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawies](https://clawhub.ai/user/clawies) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to diagnose OpenClaw or Hermes agent health, send local runtime diagnostics to Agent Hospital, and apply prescribed repairs until the issue is resolved or escalated. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The sidecar sends local agent diagnostics, logs, or workspace-derived health data to Agent Hospital. <br>
Mitigation: Use only in environments where sharing those diagnostics with the third-party service is acceptable, and review available documentation or flags for collection scope and redaction. <br>
Risk: The sidecar can make automatic local changes such as restarting services, deleting old logs or sessions, killing port conflicts, truncating large files, or checkpointing a database WAL. <br>
Mitigation: Test in a non-production environment first, keep backups for important state, and prefer repair preview or per-repair approval controls when available. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/clawies/agent-hospital) <br>
- [Agent Hospital homepage](https://api.agent-hospital.ai/.well-known/llms.txt) <br>
- [Agent Hospital full API docs](https://api.agent-hospital.ai/llms-full.txt) <br>
- [Agent Hospital dashboard](https://admin-dashboard.agent-hospital.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration, Code] <br>
**Output Format:** [Markdown with inline shell commands and repair guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npx and may trigger external sidecar actions against a local agent environment.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
