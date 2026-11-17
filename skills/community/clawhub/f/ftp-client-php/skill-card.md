## Description:

FTP/FTPS file manager via PHP proxy. Supports list, upload, download, delete, move, copy, mkdir, read, write. Works behind NAT/firewalls by routing FTP operations through an HTTP PHP proxy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erayai](https://clawhub.ai/user/erayai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage files on remote FTP or FTPS servers through a self-managed PHP HTTP proxy, especially in environments where direct FTP connections are blocked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: FTP credentials and proxy access could be exposed or misused if the PHP proxy is untrusted, unauthenticated, or configured with broad FTP privileges.

Mitigation: Use only a trusted, self-managed proxy, require a non-empty proxy API key, and configure a least-privilege FTP account.

Risk: Unsafe transport validation could expose credentials or file contents in transit.

Mitigation: Use HTTPS with proper certificate validation before handling sensitive data.

Risk: Downloaded files could overwrite local files or be saved to an unexpected location.

Mitigation: Use explicit --out paths for downloads and avoid highly sensitive data until download filename handling is fixed.

Risk: Delete operations can remove remote files or directories, including recursive directory deletion.

Mitigation: Carefully confirm delete targets and directory flags before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/erayai/skills/ftp-client-php)
- [Artifact-declared skill homepage](https://github.com/eraycc/ftp-client-skill/tree/main/ftp-client-php)
- [PHP proxy deployment reference](https://github.com/eraycc/ftp-client-skill/tree/main/ftp-proxy-php)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and FTP_PHP_CONFIG containing proxy and FTP connection settings.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
