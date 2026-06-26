## Description: <br>
Uploads a local image to Feishu and returns the image_key required for sending image messages through Feishu IM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jkzleond](https://clawhub.ai/user/jkzleond) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators working with Feishu integrations use this skill to upload a local image and obtain the image_key required before sending an image message via Feishu IM. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill caches a Feishu app bearer token in a shared temporary file, which can persist credential material on shared systems. <br>
Mitigation: Use only in trusted environments and store tokens in a private permission-restricted location, avoid persistence, or clearly document and control the cache behavior. <br>
Risk: The skill uploads local image files to Feishu using app credentials. <br>
Mitigation: Use it only with images intentionally approved for Feishu upload and with Feishu app credentials you are authorized to use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jkzleond/feishu-upload-image) <br>
- [Feishu Open Platform APIs](https://open.feishu.cn/open-apis) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Plain text image_key] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local image path and Feishu app credentials.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
