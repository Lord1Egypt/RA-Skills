## Description: <br>
将本地文件（图片、文档、视频等）上传至阿里云 OSS 并返回可直接访问的网络 URL。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[piaoleaf](https://clawhub.ai/user/piaoleaf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users who need a local file converted into a web-accessible URL can use this skill to upload images, documents, videos, audio, or archives to the configured upload service and receive a returned link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads local files to an external service endpoint, and the public or expiring nature of returned links is not fully explained. <br>
Mitigation: Use the skill only for non-sensitive files, confirm who operates the endpoint, and verify link visibility, expiration, and deletion options before uploading. <br>
Risk: The skill requires a JWT token and Device-ID, and broad or long-lived credentials could expose access if mishandled. <br>
Mitigation: Use scoped, revocable credentials where possible, store them only in the local protected configuration file, and rotate or revoke them if exposure is suspected. <br>
Risk: The artifact describes a file-size limit inconsistently with the shown upload script. <br>
Mitigation: Confirm the actual server-side size limit before relying on the skill for large uploads. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/piaoleaf/file-uploader) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text] <br>
**Output Format:** [Plain text status messages and JSON-like upload result output containing a code and URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JWT token and Device-ID for the upload service; successful output includes a web URL.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
