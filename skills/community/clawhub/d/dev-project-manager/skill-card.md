## Description: <br>
Coordinates software project management workflows for requirements gathering, SRS drafting, engineering assessment, change control, estimation, status updates, and heartbeat queue checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[encryptshawn](https://clawhub.ai/user/encryptshawn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External clients, project managers, and software delivery teams use this skill to translate requirements into structured specifications, coordinate engineering review, manage scope changes, maintain project status, and route work through project queues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to edit local project state, queue files, and project-management tasks. <br>
Mitigation: Use it only in approved workspaces and require explicit confirmation before local file, queue, or Asana mutations. <br>
Risk: The skill depends on separately installed Asana and email skills for external actions. <br>
Mitigation: Install and review those dependency skills separately, and keep their credentials isolated in the runtime environment. <br>
Risk: Heartbeat workflows can create unnecessary task checks or nudges if workspace metadata is stale. <br>
Mitigation: Keep HEARTBEAT.md and project queue metadata current, use the cheapest configured model for heartbeat checks, and stop immediately on tool or configuration failures. <br>


## Reference(s): <br>
- [Change Management & Scope Control](artifact/references/change_management.md) <br>
- [Engineer Communication Protocols](artifact/references/engineer_protocols.md) <br>
- [Estimation & Effort Communication Guide](artifact/references/estimation.md) <br>
- [Requirements Elicitation Framework](artifact/references/requirements_elicitation.md) <br>
- [SRS Standard - Software Requirements Specification](artifact/references/srs_standard.md) <br>
- [PM Communication Templates](artifact/references/templates.md) <br>
- [OpenClaw Projects](https://clawhub.ai/encryptshawn/openclaw-projects) <br>
- [Build Dev Team](https://clawhub.ai/encryptshawn/build-dev-team) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration, Shell commands] <br>
**Output Format:** [Markdown guidance, structured templates, queue messages, task instructions, and project-state updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or update local project files, queue entries, and project-management tasks when the runtime provides the required dependency skills.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
