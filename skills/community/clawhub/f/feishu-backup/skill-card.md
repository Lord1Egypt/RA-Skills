## Description: <br>
Back up files uploaded to a Feishu group chat to the local doc/backup directory with filters for count, filename, file type, and recent time range. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caigang78](https://clawhub.ai/user/caigang78) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Feishu users and agents use this skill to save matching files from a group chat into a local backup directory. It supports requests for recent uploads, multiple files, filename filters, and common file types. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Feishu downloader and argument helper used by the shell script are shared components outside the reviewed artifact. <br>
Mitigation: Install only after separately reviewing or trusting those shared Feishu components. <br>
Risk: The skill can download private chat attachments into a local backup directory. <br>
Mitigation: Confirm which Feishu account or bot is used, which chats it can access, and how long files should remain in ~/.openclaw/doc/backup. <br>
Risk: Ambiguous backup requests may select the wrong Feishu attachment. <br>
Mitigation: Require confirmation before running the backup on ambiguous requests. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Shell command execution with status text and downloaded local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads real files to ~/.openclaw/doc/backup and expects SUCCESS output with a non-empty file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
