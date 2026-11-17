## Description:

Performs FTP list, upload, download, delete, and rename operations using Node.js basic-ftp with stored or provided credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openclawzhangchong](https://clawhub.ai/user/openclawzhangchong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect FTP directories, transfer files, and perform remote file maintenance through an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext FTP can expose credentials or transferred data on untrusted networks.

Mitigation: Use only test or least-privilege FTP accounts and avoid plaintext FTP for sensitive data.

Risk: Credential fallback files can expose FTP secrets if packaged or stored with weak filesystem permissions.

Mitigation: Store credentials in a secret manager where possible, protect any local credential file, and rotate exposed credentials.

Risk: Upload, delete, rename, and broad download actions can change or copy remote files unexpectedly.

Mitigation: Require a real confirmation gate before file-changing operations or large recursive downloads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openclawzhangchong/skills/ftp-client-zc)
- [Publisher profile](https://clawhub.ai/user/openclawzhangchong)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands; list operations return JSON-formatted directory entries and mutating operations return status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FTP connection parameters or stored credentials; remote-changing operations should be gated by explicit user approval.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
