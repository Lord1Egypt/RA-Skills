## Description: <br>
Manages real-time reading, updating, and synchronization for a local Jarvis dashboard, including notes, tasks, logs, documents, automation rules, statistics, and system status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Philippeh5](https://clawhub.ai/user/Philippeh5) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Jarvis and OpenClaw users use this skill to keep a local dashboard synchronized with notes, tasks, logs, system state, documents, and automation rules through a localhost Jarvis API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change more local dashboard data than its documentation clearly discloses, including notes, tasks, logs, documents, automation rules, and system status. <br>
Mitigation: Install only after reviewing the exposed functions and enable it only for trusted Jarvis dashboard workspaces; consider restricting use to read-only workflows when state changes are not needed. <br>
Risk: The skill depends on a local Jarvis dashboard API, so an unexpected service on the configured localhost port could receive requests or return misleading state. <br>
Mitigation: Confirm the local dashboard server is trusted and running on the expected port before enabling the skill. <br>
Risk: Document deletion and automation-rule changes can remove dashboard content or alter scheduled behavior. <br>
Mitigation: Require explicit confirmation for delete operations and automation-rule changes, and keep audit logs available for review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Philippeh5/dashboard-manager2) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [JavaScript module functions and JSON-compatible API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calls a local Jarvis dashboard service and may update notes, tasks, logs, documents, automation rules, and system status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, skill.json, SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
