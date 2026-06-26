## Description: <br>
Manage software development sprints and stories in Bolt through REST API operations for stories, Kanban workflow status, blockers, dependencies, sprint digests, AI activity logs, and file attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ndhill84](https://clawhub.ai/user/ndhill84) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use this skill to manage Bolt projects, sprints, and stories from an agent session. It supports planning, status updates, blocker tracking, sprint reporting, and AI activity logging against a configured Bolt server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change Bolt project data through create, update, delete, move, batch, note, label, dependency, file, and agent-event operations. <br>
Mitigation: Use the least-privilege Bolt token available, confirm project, sprint, and story IDs before writes or bulk operations, and use dry_run where supported. <br>
Risk: Notes, agent events, and file uploads may include secrets or sensitive project data. <br>
Mitigation: Review payloads before sending and avoid uploading files or logging notes and events that contain secrets. <br>
Risk: A misconfigured BOLT_BASE_URL can direct API calls and data to an unintended Bolt server. <br>
Mitigation: Install only when the configured Bolt server is trusted, and verify BOLT_BASE_URL with the health endpoint before use. <br>


## Reference(s): <br>
- [Bolt Sprint on ClawHub](https://clawhub.ai/ndhill84/bolt-skill) <br>
- [Bolt API Reference](references/api-reference.md) <br>
- [Bolt Workflow Patterns](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bash commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces REST API requests against a configured Bolt server; write operations can change project, sprint, story, note, label, dependency, file, and agent-session data.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
