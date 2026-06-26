## Description: <br>
Run long-running, multi-step work in OpenClaw with durable state, progress updates, explicit recovery, verification gates, and optional worker-lane coordination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wonko6x9](https://clawhub.ai/user/wonko6x9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to keep multi-phase OpenClaw work recoverable across resets by recording state, milestones, events, progress, and verification before completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task snapshots, progress logs, or event logs may store sensitive work details if users put secrets into task state. <br>
Mitigation: Avoid storing secrets in task snapshots or logs and secure the underlying workspace storage. <br>
Risk: Live progress delivery can send task status externally when bound to an active chat or session. <br>
Mitigation: Prefer stdout, noop, or log-only delivery unless live OpenClaw messages are intended, and verify any chat or session binding first. <br>
Risk: Recurring tick helpers can create background status activity. <br>
Mitigation: Enable the cron helper only when recurring background ticks are explicitly wanted. <br>
Risk: The installer deletes the selected install target before linking or copying the skill. <br>
Mitigation: Review the install target carefully before running install.sh with --target. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wonko6x9/durable-task-runner) <br>
- [README](README.md) <br>
- [Quickstart](references/quickstart.md) <br>
- [Task Schema](references/task-schema.md) <br>
- [Control Levels](references/control-levels.md) <br>
- [Subagent Return Protocol](references/subagent-return-protocol.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local task snapshots, event logs, and progress logs when helper scripts are used.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
