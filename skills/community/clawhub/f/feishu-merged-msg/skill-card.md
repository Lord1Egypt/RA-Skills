## Description: <br>
Fetch and parse Feishu merged/forwarded messages (合并转发消息) when a Feishu message shows "Merged and Forwarded Message" with no readable content or sub-messages must be retrieved from a merge_forward message type. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deadblue22](https://clawhub.ai/user/deadblue22) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Feishu bot operators use this skill to retrieve sub-messages from merged or forwarded Feishu conversations and summarize the thread for a user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may expose Feishu app credentials or forwarded-message contents if credentials are read from local configuration, passed on the command line, or printed in agent-visible output. <br>
Mitigation: Use a managed secret mechanism, avoid printing or logging credentials, avoid command-line secrets where possible, and grant only the minimum Feishu read-only scope. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deadblue22/feishu-merged-msg) <br>
- [Feishu tenant access token endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu message retrieval endpoint](https://open.feishu.cn/open-apis/im/v1/messages/${MSG_ID}) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Feishu message ID plus Feishu app credentials with im:message:readonly scope.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
