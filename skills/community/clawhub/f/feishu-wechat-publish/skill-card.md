## Description: <br>
Reads Feishu documents available in the client environment and sends final article content to a relay service that creates WeChat Official Account drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shing19](https://clawhub.ai/user/shing19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators and agents use this skill to turn accessible Feishu documents, embedded images, and whiteboards into Markdown-plus-assets payloads and submit them for WeChat draft creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The relay operator receives full Feishu article contents and embedded image data. <br>
Mitigation: Use only for documents whose relay transfer is acceptable, and avoid confidential or regulated content unless the relay operator's handling practices are approved. <br>
Risk: The workflow can collect subscription tokens and WeChat AppSecret values for publishing setup. <br>
Mitigation: Confirm how secrets are stored, rotated, and revoked before use; do not expose tokens or AppSecret values in chat responses or logs. <br>
Risk: Persistent Feishu user-token binding may continue to authorize publishing actions after setup. <br>
Mitigation: Confirm the revocation process for user and WeChat bindings before installation and remove bindings when the workflow is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shing19/feishu-wechat-publish) <br>
- [Publisher profile](https://clawhub.ai/user/shing19) <br>
- [WeChat developer platform](https://developers.weixin.qq.com/platform) <br>
- [Relay publish endpoint](https://feishu.shing19.cc/api/publish) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with JSON request bodies and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces article payloads containing Markdown content and optional base64 image or whiteboard assets.] <br>

## Skill Version(s): <br>
0.5.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
