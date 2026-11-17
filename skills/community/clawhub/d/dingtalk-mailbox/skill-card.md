## Description:

Enables agents to configure and use mcporter with DingTalk mailbox MCP tools for listing mailboxes, searching and reading mail, and sending messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackeylee007](https://clawhub.ai/user/jackeylee007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users with DingTalk enterprise mailbox accounts use this skill to connect an AI assistant to mailbox search, reading, and sending workflows. It is intended for mailbox management tasks such as finding messages, reviewing message details, drafting replies, and sending email after human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables an assistant to read and send DingTalk email.

Mitigation: Use a mailbox token with limited, revocable permissions and require manual review before any email is sent.

Risk: The DingTalk mailbox access URL is stored locally in ~/.mcporter/mcporter.json.

Mitigation: Protect the mcporter configuration file as a secret and rotate or revoke the token if it may have been exposed.

Risk: The workflow depends on the globally installed mcporter package.

Mitigation: Verify the mcporter package source and version before using the skill.

## Reference(s):

- [DingTalk Mailbox MCP Service Documentation](https://help.aliyun.com/document_detail/2925708.html)
- [Agent Skills Specification](https://agentskills.io/specification)
- [mcporter Documentation](https://mcpmarket.com/zh/tools/skills/mcporter)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes DingTalk mailbox MCP tool names, argument examples, and setup guidance.]

## Skill Version(s):

1.0.0 (source: artifact/SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
