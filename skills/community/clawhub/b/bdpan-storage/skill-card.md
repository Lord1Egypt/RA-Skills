## Description: <br>
Baidu Netdisk file-management skill for uploading, downloading, transferring, sharing, listing, searching, moving, copying, renaming, and creating folders through the bdpan CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[may-yaha](https://clawhub.ai/user/may-yaha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to manage Baidu Netdisk files from an agent workflow, including cloud file operations, share-link transfers, login, logout, install, update, and uninstall flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First use may download and run a local bdpan CLI installer. <br>
Mitigation: Approve installer and updater use explicitly, review the script behavior and target paths, and prefer a trusted or sandboxed environment for first installation. <br>
Risk: The skill keeps a persistent Baidu login token on the local machine. <br>
Mitigation: Use it only on trusted machines, never expose the token or configuration file contents, and log out or uninstall when access is no longer needed. <br>
Risk: Cloud file operations and share-link actions can affect Baidu Netdisk content. <br>
Mitigation: Confirm source paths, destination paths, overwrite choices, and share-link operations before execution, especially for move, rename, upload, download, transfer, and share actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/may-yaha/bdpan-storage) <br>
- [Authentication Guide](reference/authentication.md) <br>
- [bdpan CLI Command Reference](reference/bdpan-commands.md) <br>
- [Examples](reference/examples.md) <br>
- [Usage Notes](reference/notes.md) <br>
- [Troubleshooting](reference/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include bdpan command output, JSON command output summaries, confirmation prompts, and setup guidance.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
