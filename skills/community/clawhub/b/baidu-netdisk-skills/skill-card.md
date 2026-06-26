## Description: <br>
Baidu Netdisk file management skill for uploading, downloading, transferring, sharing, searching, moving, copying, renaming, creating folders, deleting files with confirmation, and backing up or restoring agent memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wscats](https://clawhub.ai/user/wscats) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Baidu Netdisk files from an agent session through the bdpan CLI, limited to the app data area. It also supports agent memory backup, listing, and restore workflows with explicit safety checks for sensitive or destructive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth access and local credential storage for a Baidu Netdisk account. <br>
Mitigation: Install and log in only on trusted machines, do not expose bdpan configuration files or tokens, and log out or uninstall when access is no longer needed. <br>
Risk: Uploads, deletes, shares, transfers, and memory restore operations can change cloud or local data. <br>
Mitigation: Review the operation scope before approving prompts, require explicit confirmation for destructive or overwrite actions, and keep backups before restore workflows. <br>
Risk: Install and update workflows download or replace local command-line tooling. <br>
Mitigation: Run install or update only after an explicit user request, review the displayed download source and checksum information, and avoid automatic or silent updates. <br>


## Reference(s): <br>
- [Authentication Guide](reference/authentication.md) <br>
- [bdpan CLI Command Reference](reference/bdpan-commands.md) <br>
- [Usage Examples](reference/examples.md) <br>
- [Development Notes and Safety Guidance](reference/notes.md) <br>
- [Troubleshooting Guide](reference/troubleshooting.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wscats/baidu-netdisk-skills) <br>
- [Publisher Profile](https://clawhub.ai/user/wscats) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and concise status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce JSON-formatted bdpan command output when requested or when scripting workflows require it.] <br>

## Skill Version(s): <br>
1.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
