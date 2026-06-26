## Description: <br>
Uploads and manages Aliyun Drive files with refresh-token authentication, including folder creation, file search, share links, downloads, and deletion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjcly](https://clawhub.ai/user/wjcly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to manage Aliyun Drive files from local workflows, including uploads, folder creation, search, sharing, download-link retrieval, and deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access Aliyun Drive files and includes a delete action. <br>
Mitigation: Install only when this level of drive access is acceptable and confirm exact file IDs before any delete action. <br>
Risk: The skill relies on an Aliyun Drive refresh token stored in a .env file and passed to the Python helper. <br>
Mitigation: Treat the .env file as sensitive, do not commit it, restrict file permissions, and prefer versions that avoid passing refresh tokens through command-line arguments. <br>
Risk: Delete and download behavior is under-disclosed in the public skill instructions. <br>
Mitigation: Review the available actions before installing and prefer a version that clearly documents destructive and download-link behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wjcly/claw-aliyun-drive-uploader) <br>
- [Aliyun Drive token endpoint](https://auth.aliyundrive.com/v2/account/token) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON operation results plus Markdown usage instructions with shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Aliyun Drive refresh token and may return file IDs, file lists, share URLs, download URLs, or user account information.] <br>

## Skill Version(s): <br>
0.1.5 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
