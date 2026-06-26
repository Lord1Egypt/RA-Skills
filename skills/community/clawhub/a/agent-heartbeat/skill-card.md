## Description: <br>
Agent Heartbeat helps configure periodic OpenClaw agent heartbeat tasks for status checks, task review, updates, and lightweight scheduled maintenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nyxun123](https://clawhub.ai/user/nyxun123) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to define HEARTBEAT.md schedules for OpenClaw agents that need recurring task checks, online status updates, message checks, cleanup, backup, or remote sync guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring heartbeat tasks can repeat cleanup, backup, or sync actions outside the intended scope. <br>
Mitigation: Approve exact directories and remote destinations, avoid destructive cleanup by default, and keep heartbeat tasks lightweight and idempotent. <br>
Risk: Scheduled tasks can continue running after they are no longer appropriate. <br>
Mitigation: Add logging for heartbeat activity and maintain a simple way to pause or disable the schedule. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nyxun123/agent-heartbeat) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with configuration examples, shell command snippets, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance; no code runs on install.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
