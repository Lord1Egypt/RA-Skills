## Description: <br>
Manage Asana tasks, projects, briefs, status updates, custom fields, dependencies, attachments, events, and timelines via Personal Access Token (PAT). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[L-U-C-K-Y](https://clawhub.ai/user/L-U-C-K-Y) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, agents, and project managers use this skill to automate Asana personal task management and project workflows through a PAT-backed CLI. It supports task creation and updates, project briefs, status updates, custom fields, dependencies, attachments, events, and timeline shifts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a user-provided Asana PAT and can act with the permissions granted to that token. <br>
Mitigation: Use a dedicated, revocable token with the minimum permissions practical for the intended workspace and revoke it when no longer needed. <br>
Risk: Write actions can alter shared Asana projects, tasks, dependencies, dates, status updates, followers, and attachments. <br>
Mitigation: Supervise mutating commands, resolve IDs before acting, and use dry-run options for timeline shifts before applying changes. <br>
Risk: Attachment upload commands can share local files into Asana. <br>
Mitigation: Run uploads only for files the user intends to share with the target Asana task or project. <br>


## Reference(s): <br>
- [Asana Personal Access Token](https://developers.asana.com/docs/personal-access-token) <br>
- [Asana Authentication](https://developers.asana.com/docs/authentication) <br>
- [Asana Rich Text](https://developers.asana.com/docs/rich-text) <br>
- [Asana Create Attachment for Object](https://developers.asana.com/reference/createattachmentforobject) <br>
- [OpenClaw Skills](https://docs.openclaw.ai/tools/skills) <br>
- [OpenClaw Skills Config](https://docs.openclaw.ai/tools/skills-config) <br>
- [AgentSkills Format](https://agentskills.io/home) <br>
- [REFERENCE.md](references/REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Configuration instructions] <br>
**Output Format:** [JSON stdout from a Node.js CLI, with Markdown setup guidance and inline shell commands in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Asana PAT supplied through ASANA_PAT or ASANA_TOKEN; file upload commands can share local files with Asana.] <br>

## Skill Version(s): <br>
0.2.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
