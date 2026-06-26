## Description: <br>
Baidunetdisk Skill lets an agent manage Baidu Netdisk files, including listing, searching, extracting share links, transferring shared files, creating directories, renaming, moving, and deleting files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lilei0311](https://clawhub.ai/user/lilei0311) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate a Baidu Netdisk account for file discovery, share-link extraction, transfer, directory creation, and file-management tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles BDUSS and STOKEN values that act as full-account Baidu Netdisk session secrets. <br>
Mitigation: Store credentials only in trusted environments, prefer environment variables over checked-in configuration, and rotate credentials if they may have been exposed. <br>
Risk: The skill can create, move, rename, transfer, and delete cloud-storage content, and delete operations may not include a built-in confirmation step. <br>
Mitigation: Require explicit user confirmation before transfer, create, move, rename, or delete actions, and treat delete requests as irreversible unless independently confirmed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lilei0311/baidunetdisk) <br>
- [Baidu Netdisk web application](https://pan.baidu.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill requires Baidu Netdisk BDUSS and STOKEN session credentials and may return account file metadata or operation status.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata, artifact skill.json, artifact SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
