## Description: <br>
Add or remove emoji reactions on Feishu (Lark) messages, and respond to user reactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[magicaldd](https://clawhub.ai/user/magicaldd) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to add or remove Feishu message reactions, acknowledge messages with emoji, and respond naturally when users react to agent messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can add or remove visible Feishu message reactions using locally configured app credentials. <br>
Mitigation: Install only when that behavior is intended, keep Feishu app permissions limited to reaction use, and scope or disable proactive reactions where inappropriate. <br>
Risk: Weak input controls can allow unintended message IDs or emoji values to be sent to the Feishu API. <br>
Mitigation: Validate message IDs and emoji types before execution and prefer approved emoji values from the skill documentation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/magicaldd/feishu-reaction) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu message reactions API](https://open.feishu.cn/open-apis/im/v1/messages/${MSG_ID}/reactions) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and emoji type names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials configured in OpenClaw and im:message:reaction permission.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
