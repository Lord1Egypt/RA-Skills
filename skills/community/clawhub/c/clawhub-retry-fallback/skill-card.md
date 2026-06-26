## Description: <br>
Provides retry policies, exception classification, fallback execution, degradation handling, and audit logging for ClawHub agent task failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to make task workflows more resilient by retrying transient failures, selecting trusted fallbacks, degrading gracefully, and recording execution logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Retries can repeat operations and create duplicate side effects when used with non-idempotent actions. <br>
Mitigation: Use bounded retry attempts and durations, apply the helper to idempotent or deduplicated operations, and require confirmation for side-effecting backups. <br>
Risk: Fallback execution can switch work to backup functions that are untrusted or less appropriate for the task. <br>
Mitigation: Register only trusted fallback tools, review parameter mappings, and enable confirmation for sensitive switches. <br>
Risk: Audit logs and exported records can capture sensitive task details or exception messages. <br>
Mitigation: Keep logs in a protected directory, avoid logging secrets, and review exports before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaiyuelv/clawhub-retry-fallback) <br>
- [README.md](README.md) <br>
- [retry_policies.yaml](config/retry_policies.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell code examples plus configuration references.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes retry results, fallback results, degradation status, and local audit log records when used by the helper modules.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
