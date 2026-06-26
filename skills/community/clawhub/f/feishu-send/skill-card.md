## Description: <br>
Sends images, files, and audio to Feishu by guiding an agent to use curl against Feishu APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AxelHu](https://clawhub.ai/user/AxelHu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when an agent needs to upload selected local media or files and send them to a Feishu chat or user. It is suited for workflows that require direct Feishu API calls instead of a generic messaging tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload selected local files or media to Feishu. <br>
Mitigation: Verify each file path and recipient before sending, and use the skill only when file or media upload to Feishu is intended. <br>
Risk: Feishu app credentials are read from local configuration. <br>
Mitigation: Treat app credentials as secrets, use a least-privileged Feishu app or account, and set AGENT_NAME deliberately so the expected account is used. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AxelHu/feishu-send) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu image upload API](https://open.feishu.cn/open-apis/im/v1/images) <br>
- [Feishu file upload API](https://open.feishu.cn/open-apis/im/v1/files) <br>
- [Feishu message send API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Feishu app credentials and caller-provided file paths, chat IDs, user IDs, and optional audio duration.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
