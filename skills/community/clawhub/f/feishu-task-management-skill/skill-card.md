## Description: <br>
Manage Feishu tasks through a local Python toolkit with app credentials and optional OAuth user tokens for creating, inspecting, updating, completing, reopening, deleting, and changing task members while resolving people through local member data and aliases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OWRIG](https://clawhub.ai/user/OWRIG) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to manage Feishu Task records through scoped toolkit commands, including member resolution from a locally synced member table and alias mapping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security summary reports bundled Feishu credentials, a user token, and cached member data. <br>
Mitigation: Remove or replace bundled runtime configuration and cached member data before installation, and rotate any exposed app secret or token. <br>
Risk: The configured account can modify Feishu tasks and manage task members. <br>
Mitigation: Install only with a Feishu account and app scope appropriate for the intended workspace, and review state-changing commands before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/OWRIG/feishu-task-management-skill) <br>
- [API Alignment](references/api-alignment.md) <br>
- [Member Sync Troubleshooting](references/member-sync-troubleshooting.md) <br>
- [Permission Errors](references/permission-errors.md) <br>
- [Task Edge Cases](references/task-edge-cases.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, JSON, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local toolkit commands for Feishu task and member operations.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
