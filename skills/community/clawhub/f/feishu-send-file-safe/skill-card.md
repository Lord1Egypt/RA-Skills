## Description: <br>
Guides agents through Feishu/Lark message workflows for sending text, files, images, audio, video, stickers, and interactive cards using the required upload-then-send API pattern. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[icesumer-lgtm](https://clawhub.ai/user/icesumer-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to prepare Feishu/Lark API calls and shell-command workflows for sending selected messages and media to users or groups. It is intended for controlled messaging workflows that require app credentials, recipient IDs, and local file paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release tells users to run sending scripts that are not included in the package, so credentials and files may be handled by code outside the reviewed artifact. <br>
Mitigation: Review and pin the exact scripts before execution, and avoid providing real Feishu app secrets to unreviewed code. <br>
Risk: Feishu app credentials can send messages or upload files if exposed or over-permissioned. <br>
Mitigation: Use a dedicated least-privilege Feishu app, prefer environment variables over persistent config files, and rotate credentials if exposure is suspected. <br>
Risk: A wrong recipient identifier or file path could send sensitive content to an unintended user or group. <br>
Mitigation: Verify the recipient ID, message mode, and selected file before sending. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/icesumer-lgtm/feishu-send-file-safe) <br>
- [Feishu message API documentation](https://open.feishu.cn/document/server-docs/im-v1/message/create) <br>
- [Feishu image upload API](https://open.feishu.cn/document/server-docs/im-v1/image/create) <br>
- [Feishu file upload API](https://open.feishu.cn/document/server-docs/im-v1/file/create) <br>
- [Feishu Open Platform apps](https://open.feishu.cn/app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local file paths, Feishu app credentials, recipient identifiers, and Feishu message type parameters supplied by the user.] <br>

## Skill Version(s): <br>
2.0.1 (source: evidence.json release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
