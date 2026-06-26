## Description: <br>
Manages Alibaba Cloud CloudMonitor (CMS) datasets by listing, inspecting, creating, updating, deleting, and querying datasets with the aliyun CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to manage Alibaba Cloud CMS dataset lifecycle workflows and run dataset queries through confirmed aliyun CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create workspaces and create, update, or delete real Alibaba Cloud CMS datasets. <br>
Mitigation: Use a least-privilege RAM profile scoped to the intended workspace and manually confirm workspace creation, sls-project values, dataset creation, updates, and deletion before execution. <br>
Risk: The skill requires sensitive Alibaba Cloud credentials through an aliyun CLI profile. <br>
Mitigation: Avoid inline long-lived access keys, prefer verified CLI installation and profile configuration methods, and check credential status without printing secrets. <br>


## Reference(s): <br>
- [ClawHub Skill Release](https://clawhub.ai/sdk-team/alibabacloud-cms-dataset) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Related CLI Commands](references/related-commands.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Aliyun CLI Installation and Configuration Guide](references/cli-installation-guide.md) <br>
- [Official Aliyun CLI Documentation](https://help.aliyun.com/zh/cli/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Shows complete JSON API responses first, followed by concise summaries for workflow results.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
