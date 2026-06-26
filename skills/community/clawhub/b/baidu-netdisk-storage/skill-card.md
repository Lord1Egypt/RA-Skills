## Description: <br>
Baidu Drive helps agents manage Baidu Netdisk files, including uploads, downloads, transfers, sharing, search, moves, copies, renames, and folder creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[may-yaha](https://clawhub.ai/user/may-yaha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Baidu Drive files through the bdpan CLI while keeping actions scoped to the skill's application directory and requiring deliberate handling of login, update, destructive, and overwrite operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth tokens and local credentials for Baidu Drive access. <br>
Mitigation: Use only the documented login flow, avoid reading or exposing local credential files, and log out or uninstall when access is no longer needed. <br>
Risk: Uploads, downloads, transfers, shares, overwrites, and deletes can expose or alter user files. <br>
Mitigation: Review paths before file operations, require confirmation for destructive or overwrite actions, and treat generated share links as externally accessible. <br>
Risk: Install and update flows depend on trusting the Baidu CLI source. <br>
Mitigation: Install only when the user trusts the Baidu CLI source and consider reviewing or sandboxing installer behavior before use in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/may-yaha/baidu-netdisk-storage) <br>
- [Skill definition](SKILL.md) <br>
- [Authentication guide](reference/authentication.md) <br>
- [bdpan CLI command reference](reference/bdpan-commands.md) <br>
- [Usage examples](reference/examples.md) <br>
- [Usage notes](reference/notes.md) <br>
- [Troubleshooting guide](reference/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Baidu Drive share links, transfer status, and JSON-formatted CLI results when requested.] <br>

## Skill Version(s): <br>
1.4.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
