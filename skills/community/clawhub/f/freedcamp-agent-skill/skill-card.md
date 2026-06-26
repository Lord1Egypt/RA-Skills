## Description: <br>
Manage Freedcamp tasks, projects, groups, comments, notifications, and task lists via HMAC-SHA1 API credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agrublev](https://clawhub.ai/user/agrublev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to let agents manage Freedcamp workspaces through a Node.js CLI, including project discovery, task creation and updates, comments, notifications, and task lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Freedcamp API credentials and the local session cache can grant workspace access if exposed. <br>
Mitigation: Store credentials only in the intended runtime configuration, avoid printing config values, and protect or delete ~/.openclaw/skills/freedcamp-session.json when needed. <br>
Risk: Agent actions can create tasks, change task status, add comments, or mark notifications read in a real Freedcamp workspace. <br>
Mitigation: Require explicit user approval before write actions or notification state changes. <br>


## Reference(s): <br>
- [Freedcamp homepage](https://freedcamp.com) <br>
- [Freedcamp API v1](https://freedcamp.com/api/v1) <br>
- [Skill reference notes](references/REFERENCE.md) <br>
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills) <br>
- [ClawHub skill listing](https://clawhub.ai/agrublev/freedcamp-agent-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the Freedcamp CLI emits JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FREEDCAMP_API_KEY and FREEDCAMP_API_SECRET; CLI responses are JSON-only.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
