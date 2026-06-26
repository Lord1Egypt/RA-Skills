## Description: <br>
Uploads selected local files to 123pan and returns shareable short, direct, or WebDAV-backed links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solarise94](https://clawhub.ai/user/solarise94) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to upload selected local files to 123pan and receive a shareable link for distribution or download. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: 123pan API tokens, WebDAV credentials, or unrelated rclone credentials could be exposed through shared configuration files. <br>
Mitigation: Use environment variables or a local .env file outside version control, keep real tokens out of config.json, and set RCLONE_CONFIG to a dedicated 123pan-only rclone config. <br>
Risk: The selected local file is uploaded to 123pan and the generated link may be shareable outside the local environment. <br>
Mitigation: Confirm the file path and intended recipient before running the upload, and inspect the generated link before sharing it. <br>
Risk: Direct or short-direct links may expose a 123pan user ID or path details depending on link type. <br>
Mitigation: Prefer share links when privacy is important, and check whether the generated URL exposes user or path information before distribution. <br>
Risk: WebDAV/rclone workflows depend on the local rclone binary and its configured remote scope. <br>
Mitigation: Verify RCLONE_BIN points to a trusted rclone binary and use a dedicated 123pan remote rather than a general-purpose rclone configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/solarise94/123pan-upload) <br>
- [123pan developer dashboard](https://www.123pan.com/dashboard/dev) <br>
- [123pan WebDAV service](https://webdav.123pan.cn/webdav) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON upload result plus markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes success status, file ID, filename, size, generated link, and link type; upload helpers may also emit progress and retry messages.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
