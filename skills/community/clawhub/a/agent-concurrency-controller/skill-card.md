## Description: <br>
Provides serial queue scheduling, permission audit logging, and fail-closed concurrency control for OpenClaw agent spawning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suda6632](https://clawhub.ai/user/suda6632) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to queue OpenClaw sub-agent work, serialize unsafe tasks, and log permission decisions for sensitive or critical operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local queue-state and audit log files may contain sensitive task labels or operational context. <br>
Mitigation: Avoid placing secrets in task text, restrict access to ~/.openclaw/workspace, and review retained logs before sharing the workspace. <br>
Risk: Sensitive tasks are logged and allowed, while only critical tasks are held for confirmation. <br>
Mitigation: Classify external publishing, payments, destructive file operations, and other irreversible actions as critical so they require explicit confirmation. <br>
Risk: Marking tasks as concurrency-safe can bypass the default serial queue posture. <br>
Mitigation: Set is_concurrency_safe=True only after verifying resource isolation, dependency ordering, and expected side effects for that task type. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/suda6632/agent-concurrency-controller) <br>
- [Claude Code source reference](https://github.com/ultraworkers/claw-code-parity) <br>
- [CC Insider safety design reference](https://clawhub.ai/1491007406/cc-insider) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples, status strings, and JSON log records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When the controller is used, it writes local queue state and audit logs under ~/.openclaw/workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
