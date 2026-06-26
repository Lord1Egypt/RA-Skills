## Description: <br>
Sends Feishu image messages by wrapping token retrieval, image upload, and message sending scripts for local files or remote image URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kitsudog](https://clawhub.ai/user/kitsudog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to send Feishu image messages for reports, monitoring screenshots, chart delivery, and image-based bot replies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scripts need a Feishu app ID and secret that can send messages under the app's permissions. <br>
Mitigation: Use a least-privilege Feishu app, provide credentials through environment variables, and keep secrets out of repositories and logs. <br>
Risk: Remote image URLs may introduce untrusted or unexpected image content into Feishu messages. <br>
Mitigation: Use trusted image URLs and validate image sources before sending. <br>
Risk: Delivery to chat_id or user_id recipients may fail because the current message script fixes receive_id_type to open_id. <br>
Mitigation: Confirm recipient ID type before use and update the send-message flow to make receive_id_type configurable when non-open_id delivery is required. <br>
Risk: The artifact documentation overstates some supported features. <br>
Mitigation: Treat the skill as a Feishu image-message sender unless tested behavior confirms additional receive or mixed-recipient capabilities. <br>


## Reference(s): <br>
- [Feishu IM API Reference](artifact/references/api.md) <br>
- [Feishu Upload Image API](https://open.larksuite.com/document/server-docs/im-v1/image/create) <br>
- [Feishu Send Message API](https://open.larksuite.com/document/server-docs/im-v1/message/create) <br>
- [Feishu Tenant Access Token API](https://open.larksuite.com/document/server-docs/authentication-management/access-token/tenant_access_token_internal) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown guidance with Bash command examples and plain-text script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FEISHU_APP_ID and FEISHU_APP_SECRET environment variables, curl, jq, and Feishu app permissions to upload images and send messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
