## Description: <br>
Upload and send local files to Feishu chats using Feishu app credentials, supporting group chats, individual users, and email recipients. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucezhu888](https://clawhub.ai/user/brucezhu888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to upload a selected local document or archive to Feishu and send it to a group chat, individual user, or email recipient. It is intended for file-sharing workflows where Feishu message media upload is not enough for document-style files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A user or agent may upload the wrong local file or a file that is not appropriate to share in Feishu. <br>
Mitigation: Before each use, confirm the local file path and that the file is acceptable to upload to Feishu. <br>
Risk: A file may be sent to the wrong Feishu recipient if the receive_id or receive_id_type is incorrect. <br>
Mitigation: Confirm the recipient ID and type before execution, especially when using chat_id, open_id, user_id, or email values. <br>
Risk: Feishu app credentials may be over-privileged or exposed outside the intended tenant workflow. <br>
Mitigation: Use least-privilege Feishu permissions and rotate the app secret if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/brucezhu888/feishu-file-upload) <br>
- [Feishu Developer Console permissions](https://open.feishu.cn/app/YOUR_APP_ID/auth) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu file upload API](https://open.feishu.cn/open-apis/im/v1/files) <br>
- [Feishu send message API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={receive_id_type}) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Console status text and markdown-style shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, the requests library, Feishu app credentials in ~/.openclaw/openclaw.json, and optionally OPENCLAW_CHAT_ID.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
