## Description: <br>
Agent Father helps create and manage OpenClaw AI agents/employees, including Feishu chat setup, workspace configuration, onboarding files, employee records, and batch creation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meichuanyi](https://clawhub.ai/user/meichuanyi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw administrators and developers use this skill to provision AI employees, create Feishu groups, generate agent configuration and onboarding files, maintain employee records, and remove agents when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and delete OpenClaw and Feishu resources with admin-like impact. <br>
Mitigation: Use it only with intended OpenClaw workspaces and least-privilege Feishu credentials; test outside production tenants before operational use. <br>
Risk: delete-agent.sh can remove agent and workspace directories, and evidence.security notes that deletion safeguards need review. <br>
Mitigation: Back up OpenClaw workspaces and configuration before deletion, avoid --force unless paths have been reviewed, and do not run delete-agent.sh until workspace path containment and confirmation safeguards are acceptable. <br>
Risk: Employee records can include phone numbers, workspace paths, chat IDs, and session IDs. <br>
Mitigation: Review where generated employee data is stored, limit access to the OpenClaw workspace, and avoid using real personal data in tests. <br>
Risk: Feishu credentials are read from openclaw.json or environment variables and used for API calls. <br>
Mitigation: Use scoped credentials, avoid exposing configuration files or logs, and rotate credentials if a test environment is shared. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/meichuanyi/agent-father) <br>
- [QUICKSTART.md](QUICKSTART.md) <br>
- [QUICKREF.md](QUICKREF.md) <br>
- [templates.md](references/templates.md) <br>
- [create-examples.md](references/examples/create-examples.md) <br>
- [employees-sample.csv](references/examples/employees-sample.csv) <br>
- [Feishu Open API](https://open.feishu.cn/open-apis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with bash commands plus generated JSON, Markdown, and OpenClaw configuration files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Feishu APIs, create local OpenClaw workspaces and agent directories, update employee records, and delete local agent/workspace resources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
