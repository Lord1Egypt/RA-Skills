## Description: <br>
A production-ready multi-agent architecture kit for OpenClaw that provides isolated per-agent workspaces, control-plane orchestration, structured task lifecycle management, checksum-verified mailbox messaging, and auditable event logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[delibrately-cmyk](https://clawhub.ai/user/delibrately-cmyk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to install and operate a local OpenClaw multi-agent control plane with role-specific workspaces, task routing, mailbox handoffs, shared memory policy, and audit logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the blueprint modifies a target project directory by creating agent workspaces, control-plane state, task and mailbox files, logs, and shared-memory folders. <br>
Mitigation: Install only into a project directory intended for this control plane and review the generated files before letting agents use them. <br>
Risk: Autonomous agents could exceed intended authority if role rules and approval gates are not enforced by the surrounding agent runtime. <br>
Mitigation: Review the role identity files and require explicit human approval artifacts before deployment or production mutation actions. <br>


## Reference(s): <br>
- [Operations Checklist](references/operations-checklist.md) <br>
- [Local Protocol v1](assets/blueprint/docs/protocol-v1.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/delibrately-cmyk/cerberus-agent-foundry) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with bundled shell, Python, YAML, and template files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Installs a local blueprint containing role definitions, task and mailbox utilities, templates, shared-memory policy, and operational checklist material.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
