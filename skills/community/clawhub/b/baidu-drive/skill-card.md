## Description: <br>
Enables an agent to manage Baidu Drive files, including upload, download, transfer, sharing, search, move, copy, rename, folder creation, and supported agent memory backup or restore workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baidunetdiskaibot](https://clawhub.ai/user/baidunetdiskaibot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate within a Baidu Drive app folder and to back up, list, or restore supported agent memory files through Baidu Drive. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Baidu Drive authorization and uses sensitive local credentials. <br>
Mitigation: Authorize only on trusted machines, avoid shared environments, and do not expose local token or configuration contents. <br>
Risk: Cloud file operations can upload, download, overwrite, share, move, copy, rename, or delete user files. <br>
Mitigation: Review local and remote paths before execution, confirm destructive or overwrite-prone operations, and keep actions within the intended Baidu Drive app folder. <br>
Risk: Shared links, especially permanent links, can expose files beyond the current session. <br>
Mitigation: Choose the shortest practical share validity period and review link recipients before sharing. <br>
Risk: Memory restore can replace local agent instruction and memory files. <br>
Mitigation: Inspect backup contents before restoring and preserve the pre-restore local backup for rollback. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baidunetdiskaibot/baidu-drive) <br>
- [Authentication guide](reference/authentication.md) <br>
- [bdpan CLI command reference](reference/bdpan-commands.md) <br>
- [Usage examples](reference/examples.md) <br>
- [Troubleshooting guide](reference/troubleshooting.md) <br>
- [Developer notes](reference/notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and occasional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, modify, upload, download, share, back up, or restore files when the user authorizes the relevant workflow.] <br>

## Skill Version(s): <br>
1.6.0 (source: server release evidence; artifact VERSION records v1.6.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
