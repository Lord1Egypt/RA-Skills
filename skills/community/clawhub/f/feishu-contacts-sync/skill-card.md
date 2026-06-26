## Description: <br>
Sync Feishu (Lark) contacts into USER.md so the agent can identify DM senders by name. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[4ier](https://clawhub.ai/user/4ier) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure Feishu identity recognition for OpenClaw agents that receive direct messages containing open_id values but no sender names. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads Feishu app credentials from openclaw.json. <br>
Mitigation: Use a least-privileged read-only Feishu app and restrict file permissions on openclaw.json. <br>
Risk: The skill writes Feishu names and open_ids into USER.md, making directory identity data available to agent context. <br>
Mitigation: Review generated USER.md changes, restrict file permissions, and include only contacts appropriate for the workspace. <br>
Risk: Optional scheduled sync can repeatedly update agent context without manual review. <br>
Mitigation: Avoid the cron job unless recurring automated updates are intended, and review changes before restarting the gateway. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/4ier/feishu-contacts-sync) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu contact users API](https://open.feishu.cn/open-apis/contact/v3/users/find_by_department?department_id=0&page_size=50) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and USER.md table updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a Feishu open_id to name lookup table in USER.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
