## Description: <br>
Uploads user-selected local files to Baidu Pan with chunked upload, resumable transfer, progress monitoring, and remote directory creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ugpoor](https://clawhub.ai/user/ugpoor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to upload local files, including large files, into a Baidu Pan account using existing Baidu Open Platform credentials. It is useful for backup, document transfer, and other workflows that need resumable cloud uploads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads a user-chosen local file to a Baidu Pan account using credentials from a local .env file. <br>
Mitigation: Keep the .env file private and out of version control, and run the upload command only for files intended for that Baidu Pan account. <br>
Risk: An incorrect remote directory can place files in an unintended cloud location. <br>
Mitigation: Verify the remote directory argument before execution; remote paths should start with /. <br>
Risk: The --overwrite option can replace an existing cloud file. <br>
Mitigation: Use --overwrite only when replacing the existing Baidu Pan file is intended. <br>


## Reference(s): <br>
- [Baidu Open Platform application console](https://pan.baidu.com/union/console/applist) <br>
- [ClawHub skill page](https://clawhub.ai/ugpoor/baidu-pan-upload-skill) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces upload status, progress, retry, resume, and completion messages when the bundled script is run.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
