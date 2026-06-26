## Description: <br>
Performs basic FTP operations such as listing, uploading, downloading, deleting, and renaming files on a configured FTP server using Node.js. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openclawzhangchong](https://clawhub.ai/user/openclawzhangchong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this skill to run FTP file-management tasks from an agent workflow against servers they are authorized to access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use stored FTP credentials to modify, move, upload, download, or delete remote files. <br>
Mitigation: Use only credentials scoped to servers and directories the agent is intended to access, and review requested paths before running write or delete actions. <br>
Risk: The security evidence reports plaintext FTP use for credentials and file contents. <br>
Mitigation: Prefer FTPS, SFTP, or a trusted network, and avoid sending sensitive credentials or data over untrusted networks. <br>
Risk: The security evidence says the implementation lacks the safety controls claimed by the documentation. <br>
Mitigation: Review carefully before installation, remove or ignore bundled local credentials, and avoid important servers until confirmation and path controls are added. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openclawzhangchong/ftp-client-zc) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Console text and JSON emitted by FTP actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses provided credentials or stored FTP credentials to perform network file operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
