## Description: <br>
Create and populate Feishu (Lark) Bitable multidimensional tables with automated cleanup, field creation, record creation, and owner admin setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaowanqi08141999](https://clawhub.ai/user/gaowanqi08141999) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to create clean Feishu Bitable tables, define fields, add records, and grant a verified owner admin access through a configured OpenClaw Feishu integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured Feishu app has authority to create Bitables and manage document permissions. <br>
Mitigation: Use a dedicated least-privilege Feishu app, grant only the documented permissions, and install the skill only in workspaces where that authority is acceptable. <br>
Risk: An incorrect owner user_id could grant admin access to the wrong Feishu account. <br>
Mitigation: Verify the owner user_id from trusted conversation or profile context before calling the admin grant flow. <br>
Risk: Created tables may contain sensitive or incorrect structured data before sharing. <br>
Mitigation: Review generated fields, records, and sharing settings before distributing the Bitable URL. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gaowanqi08141999/feishu-bitable-creator) <br>
- [OpenClaw Feishu channel documentation](https://docs.openclaw.ai/channels/feishu) <br>
- [Feishu app console](https://open.feishu.cn/app) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, API Calls, Configuration] <br>
**Output Format:** [Markdown with TypeScript examples and Feishu Bitable operation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured Feishu app credentials through OpenClaw channel configuration.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
