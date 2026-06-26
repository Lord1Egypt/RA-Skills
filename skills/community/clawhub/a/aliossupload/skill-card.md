## Description: <br>
阿里云 OSS 文件上传工具。支持单文件上传，适用于将本地文件上传到阿里云 OSS 并获取访问链接。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JerryXn](https://clawhub.ai/user/JerryXn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to upload selected local files to an Alibaba Cloud OSS bucket and receive an access URL for the uploaded object. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected local files are uploaded to cloud storage and may expose sensitive data if the wrong path or bucket policy is used. <br>
Mitigation: Verify the exact local path before upload, keep the bucket private unless public URLs are intended, and use a dedicated RAM user limited to the intended bucket. <br>
Risk: Alibaba Cloud OSS credentials are required and could create unnecessary access if they are overprivileged. <br>
Mitigation: Store credentials securely, rotate them when needed, and grant only the OSS permissions required for the target bucket. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/JerryXn/aliossupload) <br>
- [Alibaba Cloud OSS documentation](https://help.aliyun.com/product/31815.html) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration] <br>
**Output Format:** [Text and JSON-style upload result with URL, object name, file size, elapsed time, and transfer speed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uploads selected local file contents to the configured Alibaba Cloud OSS bucket.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, package.json, clawhub.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
