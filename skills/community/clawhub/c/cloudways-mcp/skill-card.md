## Description: <br>
Operational guide for managing Cloudways servers and applications across one or several Cloudways accounts via the official Cloudways hosted MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benkalsky](https://clawhub.ai/user/benkalsky) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and agencies use this skill to manage Cloudways-hosted servers and applications, including monitoring, maintenance, onboarding audits, backups, cache operations, Git deployments, and multi-account workflows. It emphasizes read-only checks by default and explicit confirmation for write or destructive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloudways API credentials grant broad infrastructure access. <br>
Mitigation: Use dedicated per-account credentials, keep API keys and returned passwords out of shared notes or commits, and avoid printing credentials in agent responses. <br>
Risk: Write operations such as restart, restore, deployment, deletion, credential change, backup, or cache changes can disrupt production applications or data. <br>
Mitigation: Verify the account, target server or application, parameters, and expected impact before each action; require explicit user approval for writes and double confirmation for destructive actions. <br>
Risk: A multi-account setup can route an action to the wrong Cloudways account because IDs are not interchangeable across accounts. <br>
Mitigation: Confirm the account connection prefix and target resource before each tool call, and ask the user when account ownership is unclear. <br>
Risk: Some Cloudways tasks, including SSL, Let's Encrypt, SSH or MySQL IP whitelisting, and team-member management, are not exposed by the official MCP tools. <br>
Mitigation: Handle those tasks in the Cloudways Platform UI or direct Cloudways API, and use the MCP only for surrounding diagnosis or verification. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/benkalsky/cloudways-mcp) <br>
- [Cloudways MCP support article](https://support.cloudways.com/en/articles/14654372-how-to-use-cloudways-mcp-server-for-ai-based-server-management) <br>
- [Cloudways developer documentation](https://developers.cloudways.com/docs/) <br>
- [Installation](references/installation.md) <br>
- [Tools Catalog](references/tools-catalog.md) <br>
- [Workflows - Monitoring](references/workflows-monitoring.md) <br>
- [Workflows - Maintenance](references/workflows-maintenance.md) <br>
- [Workflows - Onboarding & Audit](references/workflows-onboarding.md) <br>
- [Workflows - Automation & Integration](references/workflows-automation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline command, configuration, checklist, and table examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide MCP tool selection and confirmation wording; does not itself execute Cloudways actions.] <br>

## Skill Version(s): <br>
1.2.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
