## Description: <br>
Provides Baidu Netdisk file listing, search, share extraction, share transfer, directory creation, and file management actions for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lilei0311](https://clawhub.ai/user/lilei0311) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an agent inspect and manage a Baidu Netdisk account, including searching files, extracting share links, transferring shared files, creating folders, and performing file management operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses full-access Baidu Netdisk session cookies and can act on the user's cloud storage account. <br>
Mitigation: Use a test or low-risk account where possible and store BDUSS/STOKEN only as secrets or environment variables. <br>
Risk: File management operations can delete, move, rename, or transfer cloud files. <br>
Mitigation: Manually confirm delete, move, rename, and transfer requests before allowing the skill to run. <br>
Risk: Credential disclosure could expose the Baidu Netdisk account. <br>
Mitigation: Avoid pasting BDUSS/STOKEN into chats or files and run the skill only in trusted environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lilei0311/baidunetdisk-skill) <br>
- [Baidu Netdisk web application](https://pan.baidu.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BDUSS and STOKEN credentials supplied through secrets, environment variables, or local configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
