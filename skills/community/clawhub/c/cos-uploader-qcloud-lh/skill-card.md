## Description: <br>
Receives photos from WeChat through OpenClaw and uploads them to Tencent Cloud COS low-frequency storage with year/month archive paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jingronzhao](https://clawhub.ai/user/jingronzhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this OpenClaw skill to receive photos through WeChat and upload them into Tencent Cloud COS with automated date-based organization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Message-specified local file paths can be uploaded to Tencent COS without tight restriction to the OpenClaw inbound media cache. <br>
Mitigation: Validate canonical paths against the OpenClaw inbound media cache and verify actual image content before upload. <br>
Risk: COS credentials and stored photos can be exposed if permissions or local secret files are not protected. <br>
Mitigation: Use a least-privilege Tencent COS sub-account limited to the intended bucket, keep the bucket private, protect local secrets, and rotate credentials. <br>
Risk: Photos sent through WeChat may contain personal data. <br>
Mitigation: Document consent, retention, and deletion expectations before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jingronzhao/cos-uploader-qcloud-lh) <br>
- [Tencent Cloud COS bucket console](https://console.cloud.tencent.com/cos/bucket) <br>
- [Tencent Cloud CAM API keys](https://console.cloud.tencent.com/cam/capi) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Configuration] <br>
**Output Format:** [Plain text status messages with Tencent COS upload side effects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uploads image files to Tencent COS using the configured storage class and date-based object keys.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
