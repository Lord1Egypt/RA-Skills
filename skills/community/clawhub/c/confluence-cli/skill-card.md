## Description:

Interact with Confluence Cloud from the command line for reading, creating, updating, searching, exporting, and managing pages, attachments, labels, and comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hochej](https://clawhub.ai/user/hochej)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to work with Confluence Cloud content through confcli, including page lookup, search, edits, exports, and related content management tasks. It is also useful for agents that need to propose or run explicit Confluence CLI commands after authentication is configured outside the conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install instructions execute a mutable remote GitHub shell script directly with curl piped to sh.

Mitigation: Inspect a pinned release or verified installer before installation instead of running the mutable installer directly.

Risk: The skill can guide write, delete, purge, attachment, label, comment, and copy-tree actions in Confluence.

Mitigation: Run write or destructive actions only after a clear user request and use dry-run previews where supported.

Risk: Confluence authentication depends on domain, email, and API token credentials.

Mitigation: Configure credentials through environment variables or interactive login and do not paste tokens into the conversation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hochej/skills/confluence-cli)
- [Atlassian API tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
- [confcli install script referenced by artifact](https://raw.githubusercontent.com/hochej/confcli/main/install.sh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON, table, or Markdown output-format flags for confcli commands.]

## Skill Version(s):

0.2.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
