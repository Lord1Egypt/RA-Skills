## Description:

DingTalk Docs helps agents search, create, read, write, and organize DingTalk Cloud Docs while avoiding unsupported workflows such as calendar, messaging, approval, and multidimensional-table management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aliramw](https://clawhub.ai/user/aliramw)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and operational teams use this skill to manage DingTalk Cloud Docs through an agent: locating accessible documents, creating documents or folders, writing Markdown content, and conditionally reading document content when the service exposes the read tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a token-bearing DingTalk document service URL.

Mitigation: Store the URL with mcporter configuration or a protected environment variable, and avoid exposing it in shell history, logs, or shared files.

Risk: The skill can create, overwrite, or append cloud document content.

Mitigation: Confirm the target document ID and update mode before writing, especially when updateType=0 would replace existing content.

Risk: Ambiguous requests for tables or multidimensional tables can select the wrong DingTalk node type.

Mitigation: Ask the user to choose the intended node type before calling create_dentry_under_node, and pass accessType as a string.

Risk: Local import and export helpers read or write workspace files.

Mitigation: Review file contents and destinations before import or export, and rely on the documented workspace path, extension, and size checks.

Risk: The mcporter binary is required for document operations.

Mitigation: Pin and verify mcporter before global installation or execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aliramw/skills/dingtalk-docs)
- [DingTalk Docs Repository](https://github.com/aliramw/dingtalk-docs)
- [DingTalk MCP Service](https://mcp.dingtalk.com)
- [API Reference](references/api-reference.md)
- [Error Codes](references/error-codes.md)
- [Security Test Report](tests/TEST_REPORT.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON argument examples and shell commands; helper scripts read or write workspace Markdown and text files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses mcporter and DINGTALK_MCP_DOCS_URL. Document reading is conditional when the DingTalk service has not exposed get_document_content_by_url.]

## Skill Version(s):

0.3.4 (source: SKILL.md frontmatter, package.json, CHANGELOG, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
