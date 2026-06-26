## Description: <br>
Aliyun OSS file upload tool for secure, efficient file uploads and temporary link generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jixsonwang](https://clawhub.ai/user/jixsonwang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to upload local files to Aliyun OSS, batch upload files, search bucket objects by filename, and return temporary access links for shared workflow outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads local files to an Aliyun OSS bucket and can expose sensitive data if pointed at the wrong file or bucket path. <br>
Mitigation: Review upload targets before execution and use bucket prefixes and permissions that match the intended data-sharing scope. <br>
Risk: The skill uses Aliyun OSS access credentials stored in /root/.openclaw/aliyun-oss-config.json. <br>
Mitigation: Use a dedicated least-privilege RAM user, protect the config file, rotate keys regularly, and avoid broad ListObjects permissions where possible. <br>
Risk: Shared URLs may provide unintended access if public-read mode or non-temporary links are used. <br>
Mitigation: Avoid public-read mode for sensitive files and verify that shared links are presigned and temporary before sending them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jixsonwang/aliyun-oss) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with command examples, JSON configuration, OSS object paths, and URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return presigned temporary URLs, standard OSS URLs, upload status, file metadata, and error messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
