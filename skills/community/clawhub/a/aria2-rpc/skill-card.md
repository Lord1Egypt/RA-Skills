## Description:

Remote control for aria2 download service via JSON-RPC 2.0. Supports adding downloads (HTTP/FTP/Torrent/Magnet), querying task status, pausing/resuming, and removing tasks. Works with local or remote aria2 instances.

This skill is ready for commercial/non-commercial use.

## Publisher:

[killgfat](https://clawhub.ai/user/killgfat)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to manage local or remote aria2 download services through JSON-RPC, including adding downloads, checking status, pausing or resuming tasks, removing tasks, and changing aria2 options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can administer an aria2 RPC service, and the security evidence notes that setup and examples may encourage exposing that service.

Mitigation: Keep aria2 RPC bound to localhost when possible, and use an SSH tunnel, VPN, or HTTPS for remote access.

Risk: The security evidence notes that RPC secrets may be sent over plaintext HTTP or appear in command history or shared configuration files.

Mitigation: Use a strong unique RPC secret, prefer protected transport for remote use, and avoid placing secrets directly in shared files or shell history.

Risk: Remove, force-remove, and bulk cleanup commands can affect the wrong download when a task GID is mistaken.

Mitigation: Verify task GIDs with status or listing commands before running destructive or bulk cleanup operations.

## Reference(s):

- [aria2 Project Homepage](https://aria2.github.io)
- [aria2 RPC Interface Documentation](https://aria2.github.io/manual/en/html/aria2c.html#rpc-interface)
- [aria2 Configuration Options](https://aria2.github.io/manual/en/html/aria2c.html#id3)
- [Quickstart](references/QUICKSTART.md)
- [Configuration Guide](references/CONFIG_GUIDE.md)
- [Usage Examples](references/USAGE.md)
- [API Reference](references/API_REFERENCE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an aria2 RPC endpoint and optional RPC secret; command output depends on the aria2 server state.]

## Skill Version(s):

0.1.2 (source: clawhub.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
