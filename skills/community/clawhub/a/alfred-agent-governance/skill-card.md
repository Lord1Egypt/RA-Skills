## Description: <br>
Provides OpenClaw agent governance guidance and examples for YAML-based policy checks, audit logging, and kill-switch operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sabatech-dev](https://clawhub.ai/user/sabatech-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to plan runtime governance for OpenClaw agents, including policy checks before tool execution, audit records, and emergency session-stop procedures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact describes rate-limit, approval, resource-limit, and audit-integrity controls that are not fully enforced by the included examples. <br>
Mitigation: Implement and test those controls before relying on the skill for governance decisions. <br>
Risk: Audit logs may not provide sufficient integrity, permission, or retention guarantees by default. <br>
Mitigation: Set appropriate filesystem permissions, retention rules, and tamper-evidence controls for generated audit logs. <br>


## Reference(s): <br>
- [Alfred Agent Governance on ClawHub](https://clawhub.ai/sabatech-dev/alfred-agent-governance) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with YAML, Python, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes governance concepts, example configuration, policy-check snippets, audit-log format, and operational commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
