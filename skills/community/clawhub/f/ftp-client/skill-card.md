## Description: <br>
FTP/FTPS client skill that connects to FTP servers and performs file operations including list, upload, download, delete, move, copy, mkdir, and read. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erayai](https://clawhub.ai/user/erayai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect and manage files on configured FTP or FTPS servers. It is suited for agent-assisted remote file transfer and directory maintenance where the agent is trusted with scoped FTP credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-accessible FTP operations can expose or alter remote server files. <br>
Mitigation: Use a least-privilege FTP account scoped to the specific directory and data needed for the task. <br>
Risk: Weak transport defaults may reduce confidentiality or server authenticity for FTP/FTPS connections. <br>
Mitigation: Prefer FTPS and verify certificate validation externally or fix it before using sensitive credentials. <br>
Risk: Upload, move, and delete operations can cause unintended remote data changes. <br>
Mitigation: Review target paths and intended operations before executing destructive or write commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/erayai/ftp-client) <br>
- [Publisher profile](https://clawhub.ai/user/erayai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Files, Text] <br>
**Output Format:** [Markdown with inline bash code blocks and command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and FTP_CONNECTION; file transfer commands may read, write, move, copy, or delete remote FTP server content.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
