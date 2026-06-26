## Description: <br>
Ftp Sync documents and wraps a Python command-line helper for FTP/SFTP-style local and remote file synchronization, incremental backup, sync reporting, and difference checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SxLiuYu](https://clawhub.ai/user/SxLiuYu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and server administrators can use this skill for guidance and command examples around local-to-remote or remote-to-local file synchronization workflows for website maintenance and server management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper describes backup, deployment, and remote synchronization workflows, but the implementation does not complete real FTP/SFTP transfer behavior. <br>
Mitigation: Review and test the implementation in a non-production environment before relying on it for backup, deployment, or synchronization tasks. <br>
Risk: Example commands include password and privileged-account patterns that can expose credentials or increase impact if misused. <br>
Mitigation: Use key-based or prompted authentication, least-privilege server accounts, and avoid placing real passwords directly in command-line arguments. <br>
Risk: Server-sync commands can affect the wrong remote path or overwrite expected content if targets are not checked first. <br>
Mitigation: Run dry-run or diff checks first and verify host, account, and target paths before production use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/SxLiuYu/ftp-sync) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/SxLiuYu) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash code blocks and terminal-style text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dry-run, upload, download, or diff command examples for a Python helper script.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
