## Description:

Set up a Tencent enterprise email MCP connector for WorkBuddy, replacing mcp-email with a custom server that reads, searches, fetches, and sends email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wildbyteai](https://clawhub.ai/user/wildbyteai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and WorkBuddy users use this skill to install and configure a Tencent enterprise email MCP connector for reading, searching, fetching, and sending mailbox content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connector is presented as read and search focused, but the referenced server also exposes a send_email tool.

Mitigation: Disclose or remove the send_email capability before deployment, and require explicit approval before any email is sent.

Risk: The setup disables TLS certificate verification for IMAP and SMTP connections.

Mitigation: Restore certificate verification where possible, investigate certificate trust issues directly, and rotate any auth code used with the insecure configuration.

Risk: The setup stores an enterprise mailbox auth code in MCP environment configuration.

Mitigation: Use the least-privileged auth code available, restrict access to the configuration file, avoid plaintext storage where supported, and rotate credentials after testing.

Risk: Dependencies are installed without version pins.

Mitigation: Pin and review dependencies before production use, and scan updates before accepting them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wildbyteai/skills/exmail-mcp-setup)
- [Publisher profile](https://clawhub.ai/user/wildbyteai)
- [Reference MCP server code](artifact/references/index.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON, JavaScript, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup guidance for a WorkBuddy MCP server that requires mailbox credentials and connector trust before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
