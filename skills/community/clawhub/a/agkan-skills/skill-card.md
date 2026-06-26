## Description: <br>
Use when managing tasks with the agkan CLI tool - creating, listing, updating tasks, managing tags, blocking relationships, or tracking project progress with the kanban board. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gendosu](https://clawhub.ai/user/gendosu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to manage project work through the agkan CLI, including task creation, status updates, blocking relationships, tags, metadata, and kanban-style progress tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides agents to update or delete local task records through the agkan CLI. <br>
Mitigation: Install it only where the agkan CLI and target project database are trusted; review the target task or tag before delete commands and prefer closing tasks when history may be needed. <br>
Risk: Commands may affect an unintended project database if the agkan database path is misconfigured. <br>
Mitigation: Confirm the project `.agkan.yml` path or `AGENT_KANBAN_DB_PATH` setting before running mutating commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gendosu/agkan-skills) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with CLI command examples and JSON schema examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task IDs, status names, tag names, assignees, metadata keys, and project database path configuration.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
