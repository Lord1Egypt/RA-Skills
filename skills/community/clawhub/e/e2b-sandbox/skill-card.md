## Description: <br>
Spin up and manage E2B cloud sandboxes for agent work when an OpenClaw agent needs an isolated remote Linux sandbox instead of the local workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create, reconnect to, run one-shot commands in, expose ports for, snapshot, and terminate E2B cloud sandboxes instead of running isolated or risky work on the local host. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires the sensitive E2B_API_KEY credential. <br>
Mitigation: Configure E2B_API_KEY securely through the environment or vault and avoid placing it in prompts, logs, or committed files. <br>
Risk: Sandbox command execution can run user-directed commands in cloud environments. <br>
Mitigation: Review commands before execution and supervise sandbox use when working with sensitive projects. <br>
Risk: Public port exposure can make sandbox services reachable outside the local workspace. <br>
Mitigation: Expose only intentional ports and review hosted services before sharing or relying on public URLs. <br>
Risk: Snapshots can preserve prepared environments and their state. <br>
Mitigation: Check sandbox contents before snapshotting and avoid snapshotting secrets or sensitive project data. <br>
Risk: Dependency installation is part of the helper workflow. <br>
Mitigation: Review dependency installation behavior before use in sensitive projects. <br>


## Reference(s): <br>
- [E2B Notes](references/e2b-notes.md) <br>
- [ClawHub skill page](https://clawhub.ai/maverick-software/e2b-sandbox) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, MCP tool calls, and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires E2B_API_KEY and may create local MCPorter configuration and sandbox state files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
