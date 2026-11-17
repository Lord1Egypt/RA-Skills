## Description:

Manage Dropbox files securely with OAuth 2.0 PKCE via CLI or MCP server, supporting upload, download, search, delete, and account info operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryanlisse](https://clawhub.ai/user/ryanlisse)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to connect an MCP-capable agent or CLI workflow to Dropbox for listing, searching, uploading, downloading, deleting, reading text files, and account lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad ability to read, change, upload, download, and delete Dropbox files.

Mitigation: Install only when that access is appropriate, use narrowly scoped Dropbox credentials, and review destructive or sensitive file operations before execution.

Risk: Persistent Dropbox credentials may be exposed if legacy token setup or plaintext token files are used.

Mitigation: Prefer the documented Swift and Keychain OAuth path, avoid the npx-based legacy setup unless the package is pinned and reviewed, and harden or avoid plaintext rclone token files.

## Reference(s):

- [Dropbox Manager on ClawHub](https://clawhub.ai/ryanlisse/skills/dropbox)
- [MCP setup guide](references/mcp-setup.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown documentation with JSON MCP responses and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Dropbox application credentials and access scoped to the intended Dropbox account or files.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/SKILL.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
