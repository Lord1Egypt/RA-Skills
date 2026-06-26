## Description: <br>
Agent Extract helps split a skill or function out of a main OpenClaw agent into an independent agent with isolated session, workspace, memory, identity, and heartbeat configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kings0527](https://clawhub.ai/user/kings0527) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to move a feature from a main OpenClaw agent into a separate agent while preserving session, workspace, identity, memory, channel, and heartbeat boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide changes to local OpenClaw agent configuration and persistent cron jobs. <br>
Mitigation: Back up ~/.openclaw before use and review each proposed configuration and cron change before applying it. <br>
Risk: The workflow may duplicate sensitive identity and memory files into a new workspace. <br>
Mitigation: Review the files selected for copying and omit sensitive memory or identity content that the new agent does not need. <br>
Risk: Heartbeat changes can remove or overwrite unrelated ongoing tasks if applied too broadly. <br>
Mitigation: Manually preserve unrelated HEARTBEAT.md tasks and verify the main agent heartbeat after separation. <br>
Risk: Rollback instructions include deletion paths that could remove the wrong workspace if identifiers are incorrect. <br>
Mitigation: Use a simple agent ID and verify all resolved paths before running any removal command. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kings0527/agent-extract) <br>
- [Publisher profile](https://clawhub.ai/user/kings0527) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes verification and rollback steps for OpenClaw agent separation workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
