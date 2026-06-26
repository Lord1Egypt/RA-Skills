## Description: <br>
FTP/FTPS file manager via PHP proxy. Supports list, upload, download, delete, move, copy, mkdir, read, write. Works behind NAT/firewalls (e.g. HuggingFace) by routing FTP operations through an HTTP PHP proxy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erayai](https://clawhub.ai/user/erayai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage files and directories on FTP or FTPS servers from an agent environment, including listing, uploading, downloading, reading, writing, moving, copying, deleting, and creating directories through a PHP HTTP proxy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles FTP credentials and file transfers through a PHP proxy. <br>
Mitigation: Install only when the PHP proxy and FTP account are controlled and trusted; use a least-privilege FTP account. <br>
Risk: The proxy API key can be left empty according to the configuration format. <br>
Mitigation: Set a non-empty proxy API key and protect FTP_PHP_CONFIG as a secret. <br>
Risk: File operations can delete, overwrite, move, or recursively remove remote content. <br>
Mitigation: Confirm target paths and destructive operations before execution. <br>
Risk: The proxy connection may use HTTPS with certificate verification disabled by the client implementation. <br>
Mitigation: Prefer HTTPS with a valid certificate and deploy the proxy in a trusted network location. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/erayai/ftp-client-php) <br>
- [Skill homepage](https://github.com/eraycc/ftp-client-skill/tree/main/ftp-client-php) <br>
- [PHP proxy deployment reference](https://github.com/eraycc/ftp-client-skill/tree/main/ftp-proxy-php) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, configuration] <br>
**Output Format:** [CLI text output, local downloaded files, and remote FTP or FTPS file changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and FTP_PHP_CONFIG with PHP proxy and FTP account connection details.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
