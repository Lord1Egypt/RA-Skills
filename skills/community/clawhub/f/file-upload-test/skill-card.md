## Description: <br>
上传文件到内部 BS3 存储（免签名）。Use when user asks to upload files, images, documents to storage, or get a shareable URL for a file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bagayalu](https://clawhub.ai/user/bagayalu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and internal users use this skill to upload local files or byte content to an internal BS3-compatible storage endpoint and return a shareable URL. <br>

### Deployment Geography for Use: <br>
Internal network environments where the configured BS3 endpoint is reachable <br>

## Known Risks and Mitigations: <br>
Risk: The storage endpoint, bucket, CDN domain, and retention behavior may not be clear enough for sensitive file-sharing decisions. <br>
Mitigation: Verify the configured endpoint, bucket, returned domain, and retention policy before enabling the skill for users. <br>
Risk: Uploaded files may be exposed through shareable URLs or retained only temporarily. <br>
Mitigation: Do not use the skill for secrets, personal data, confidential reports, or regulated files unless destination access controls and retention are confirmed. <br>
Risk: The skill depends on an internal network and BS3-compatible service availability. <br>
Mitigation: Use it only in environments that can reach the configured internal endpoint and have the required Python dependencies installed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bagayalu/file-upload-test) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/bagayalu) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, guidance] <br>
**Output Format:** [Plain text URL with a retention warning; optional Markdown guidance and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returned URLs are described as temporary and valid for 7 days.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
