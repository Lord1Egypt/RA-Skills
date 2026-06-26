## Description: <br>
Manage Dropbox files through an MCP server or Swift CLI for listing, searching, reading, uploading, downloading, deleting, and account lookup operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RyanLisse](https://clawhub.ai/user/RyanLisse) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to connect MCP clients or a Swift CLI to Dropbox for file-management workflows. It is suited to workflows where the operator is comfortable granting Dropbox read/write access and confirming transfer or destructive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dropbox credentials and read/write file access can expose or alter user data. <br>
Mitigation: Grant only the required Dropbox scopes, store tokens securely, and require confirmation before uploads, downloads, deletes, overwrites, or sync operations. <br>
Risk: The bundled setup guide references an unpinned npm MCP server that would receive Dropbox credentials. <br>
Mitigation: Prefer the documented Swift Dropbook build path, and review any package before giving it Dropbox tokens. <br>
Risk: Bulk transfer and sync commands can overwrite or delete files if paths or direction are wrong. <br>
Mitigation: Validate paths first, use dry runs for sync-style operations, and confirm the source and destination before running rclone or destructive Dropbox actions. <br>


## Reference(s): <br>
- [Dropbox MCP Setup Guide](artifact/references/mcp-setup.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/RyanLisse/dropbox) <br>
- [Dropbox API Documentation](https://www.dropbox.com/developers/documentation) <br>
- [rclone Dropbox Documentation](https://rclone.org/dropbox/) <br>
- [RFC 7636 - Proof Key for Code Exchange](https://datatracker.ietf.org/doc/html/rfc7636) <br>
- [RFC 9700 - OAuth 2.0 Security Best Current Practice](https://datatracker.ietf.org/doc/html/rfc9700) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and inline shell commands; MCP tool responses may be JSON or text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Dropbox app credentials and user confirmation for uploads, downloads, deletes, overwrites, and sync operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
