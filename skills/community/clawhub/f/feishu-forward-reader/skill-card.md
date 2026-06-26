## Description: <br>
读取和解析飞书合并转发消息(merge_forward)的详细内容。当收到飞书转发消息显示为"Merged and Forwarded Message"时使用此 skill 获取原始消息内容。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[konce](https://clawhub.ai/user/konce) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators who use Feishu with OpenClaw use this skill to recover the original contents of merged-forward messages that otherwise appear only as "Merged and Forwarded Message". It fetches message details through the Feishu API and formats forwarded sub-messages into readable text or JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Feishu app credentials to read message contents that the app can access. <br>
Mitigation: Install only from a trusted publisher, protect the app secret, and review the Feishu app permissions before use. <br>
Risk: Optional sender-name lookup can access user basic profile information when the Feishu app has contact permissions. <br>
Mitigation: Use --no-names when sender display names are not needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/konce/feishu-forward-reader) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu message retrieval API](https://open.feishu.cn/open-apis/im/v1/messages/{message_id}) <br>
- [Feishu user lookup API](https://open.feishu.cn/open-apis/contact/v3/users/{open_id}?user_id_type=open_id) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON, with Markdown usage examples and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can omit sender-name lookup with --no-names; raw JSON is available through the shell helper.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
