## Description:

Complete Feishu (Lark) skills collection for Claude Code and OpenClaw agents, covering document management, messaging, spreadsheets, Bitable records, interactive cards, bot bridging, cross-group memory, and leave request workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hewenqiang](https://clawhub.ai/user/hewenqiang)

### License/Terms of Use:


## Use Case:

Developers and teams use this skill kit to connect agents with Feishu/Lark workspaces for document publishing and editing, message sending, spreadsheet and Bitable operations, bot conversations, memory recall, and guided leave requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundle uses Feishu app credentials and may also use a local gateway token.

Mitigation: Store secrets outside the skill files, restrict file permissions, rotate exposed credentials, and grant only the Feishu scopes needed for the selected skills.

Risk: The bridge can run persistently and connect Feishu messages to a local agent gateway.

Mitigation: Enable the bridge only after review, restrict allowed senders and chats, monitor logs, and confirm that persistent LaunchAgent behavior is acceptable.

Risk: The security scan reports exploitable command-handling flaws in card scripts.

Mitigation: Review and replace shell-string execution before use, then retest the affected messaging and card workflows.

Risk: The MCP server setup can provide broad local-agent access to Feishu workspace data.

Mitigation: Review the MCP server repository at a pinned commit, use least-privilege Feishu app permissions, and deploy only the skills required for the intended workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hewenqiang/skills/feishu-skills-kit)
- [Feishu Open Platform](https://open.feishu.cn/app)
- [Feishu Server API Documentation](https://open.feishu.cn/document/server-docs/api-call-guide/server-api-list)
- [Feishu Doc Editor API Guide](skills/feishu-doc-editor/references/api-guide.md)
- [Feishu Doc Editor Permission Setup](skills/feishu-doc-editor/references/permission-setup.md)
- [Feishu Doc Editor Common Errors](skills/feishu-doc-editor/references/common-errors.md)
- [Feishu Docx PowerWrite Templates](skills/feishu-docx-powerwrite/references/templates.md)
- [Feishu Docx PowerWrite Troubleshooting](skills/feishu-docx-powerwrite/references/troubleshooting.md)
- [Feishu Sheets API Reference](skills/feishu-sheets-skill/references/api-reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code blocks, shell commands, JSON configuration, and API-oriented instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require Feishu app credentials, Feishu workspace permissions, MCP server configuration, Node.js, Python, npm, and optional local bridge execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
