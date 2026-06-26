## Description: <br>
Catfee SSH helps an agent connect to remote servers over SSH with user-provided password credentials to run commands, inspect configurations, diagnose services, and perform file operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[glory904649854](https://clawhub.ai/user/glory904649854) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent connect to user-specified servers over SSH, inspect system and service state, view files and logs, and run operational commands. It is most relevant for Windows environments where PowerShell and Posh-SSH are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad password-based SSH control over remote servers. <br>
Mitigation: Install only when remote server operation is intended, use a least-privilege account instead of root, prefer SSH keys where possible, and verify the SSH host fingerprint before connecting. <br>
Risk: Remote commands can restart services, reload configuration, write files, delete data, or otherwise change server state. <br>
Mitigation: Require explicit approval before any sudo command, service restart or reload, file write, deletion, or other state-changing operation. <br>
Risk: Password-based access can expose sensitive credentials if mishandled. <br>
Mitigation: Provide credentials only for the active session, avoid logging or echoing secrets, and close SSH sessions after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/glory904649854/catfee-ssh) <br>
- [Publisher profile](https://clawhub.ai/user/glory904649854) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with PowerShell and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill depends on user-provided SSH connection details and may propose or run state-changing remote commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
