## Description:

FTP/FTPS client skill. Connect to FTP servers and perform file operations (list, upload, download, delete, move, copy, mkdir, read). Supports FTP and FTPS (explicit/implicit TLS).

This skill is ready for commercial/non-commercial use.

## Publisher:

[erayai](https://clawhub.ai/user/erayai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect an agent to FTP or FTPS servers and manage remote files, including listing, upload, download, delete, move, copy, directory creation, content reading, and file info checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials and file contents may be exposed when plain FTP is used on untrusted networks.

Mitigation: Use only a least-privileged FTP account and prefer FTPS after confirming certificate validation is acceptable for the deployment.

Risk: Remote delete and recursive directory operations can remove more data than intended.

Mitigation: Confirm remote paths before delete or recursive operations and avoid broad paths for accounts with write access.

Risk: Malformed connection values may reveal sensitive configuration in error output.

Mitigation: Rotate credentials if malformed FTP_CONNECTION values may have been logged.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/erayai/skills/ftp-client)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and an FTP_CONNECTION environment variable.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
