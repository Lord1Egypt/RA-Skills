## Description: <br>
AgentFlow workflow management skill for managing project, requirement, task, status-transition, search, and attachment-upload workflows through the AgentFlow service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[glory904649854](https://clawhub.ai/user/glory904649854) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project teams use this skill to create and manage AgentFlow projects, requirements, tasks, status transitions, timelines, searches, and related file attachments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project details, requirements, tasks, and selected file contents may be sent to a hard-coded plaintext AgentFlow HTTP service. <br>
Mitigation: Use only when the AgentFlow service is trusted, and avoid sensitive documents until HTTPS, authentication, workspace scoping, and data retention are documented. <br>
Risk: The skill can create, update, delete, transition, and upload data in the remote AgentFlow service. <br>
Mitigation: Require explicit user confirmation before syncing, uploading, deleting, or changing statuses. <br>
Risk: Unclear workspace scoping can make accidental updates to the wrong project, requirement, or task more likely. <br>
Mitigation: Verify target project, requirement, task, and entity type identifiers before every remote write or file upload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/glory904649854/catfee-agent-flow) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Text, Markdown] <br>
**Output Format:** [Markdown instructions with shell commands and JSON or text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce markdown task files and may modify or upload files to remote AgentFlow records when commands are executed.] <br>

## Skill Version(s): <br>
1.9.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
