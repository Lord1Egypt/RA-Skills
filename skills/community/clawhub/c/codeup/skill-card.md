## Description: <br>
Codeup lets an agent manage Alibaba Cloud Yunxiao Codeup repositories, branches, files, merge requests, organizations, departments, members, and roles through a Python CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yu-xiao-sheng](https://clawhub.ai/user/yu-xiao-sheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to query and manage Codeup repositories, merge requests, and organization membership from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent live authority to delete branches or files, approve or reject reviews, close or merge merge requests, and remove source branches. <br>
Mitigation: Use a least-privilege token, start with read-only access when possible, and require explicit human approval before destructive or approval-changing commands. <br>
Risk: The required Codeup access token can grant repository and organization access if exposed. <br>
Mitigation: Store YUNXIAO_ACCESS_TOKEN only in the runtime environment, avoid logging it, and rotate or revoke it according to the organization's credential policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yu-xiao-sheng/codeup) <br>
- [Code Management API Reference](references/code-management.md) <br>
- [Organization Management API Reference](references/organization-management.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires YUNXIAO_ACCESS_TOKEN; commands operate on live Codeup resources according to the token permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
