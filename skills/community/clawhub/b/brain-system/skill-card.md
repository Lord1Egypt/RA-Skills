## Description: <br>
人脑系统 is a brain-inspired operating protocol for agents that organizes attention, memory, task control, reflection, verification, and self-maintenance for longer-running collaboration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaxia01-1](https://clawhub.ai/user/xiaxia01-1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add structured long-term memory, context checkpoints, task queues, status dashboards, and post-task consolidation to an AI assistant. It is intended for sustained project work, repeated troubleshooting, preference learning, and self-maintenance workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The memory, checkpoint, consolidation, dream, and backup flows can copy broad local memory or authority state into durable files. <br>
Mitigation: Before running those flows, remove or redact authority.json and other sensitive files, and review generated state before sharing or retaining it. <br>
Risk: The hot-reload watcher can run as long-lived automatic maintenance and generate additional checkpoint or consolidation state. <br>
Mitigation: Enable the watcher only intentionally, avoid cron-style maintenance unless it is actively managed, and keep a clear stop and cleanup procedure. <br>
Risk: The security scan verdict is suspicious because the skill can preserve local memory and self-maintenance state beyond the current interaction. <br>
Mitigation: Install only when a local agent memory system is intended, and scan and review the skill before deployment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with optional local script commands and generated state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or read local memory, checkpoint, consolidation, backup, dashboard, and task-queue files when the operator runs the bundled scripts.] <br>

## Skill Version(s): <br>
0.1.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
