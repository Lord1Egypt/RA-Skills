## Description:

Dingtalk Docs helps an agent create, search, read, and update DingTalk cloud documents and folders while avoiding unrelated workflows such as schedules, messages, approvals, and multidimensional tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chayjan](https://clawhub.ai/user/chayjan)

### License/Terms of Use:

MIT

## Use Case:

Employees and developers use this skill to manage DingTalk cloud documents: create documents and folders, search accessible documents, read content by URL, and write Markdown content with explicit overwrite or append handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read, create, and modify DingTalk cloud documents, including overwrite writes.

Mitigation: Review each requested document action before execution and require explicit confirmation before overwrite writes.

Risk: The skill can create non-document DingTalk node types such as tables or PPTs.

Mitigation: Confirm the intended node type with the user before creation, especially when a request mentions a table.

Risk: The skill relies on an unpinned global mcporter helper.

Mitigation: Prefer a pinned local mcporter installation and review the configured DingTalk service URL before use.

Risk: Export operations can overwrite local files.

Mitigation: Use non-sensitive workspace paths for exports and review the destination path before writing.

## Reference(s):

- [DingTalk Docs API Reference](references/api-reference.md)
- [DingTalk Docs Error Codes](references/error-codes.md)
- [DingTalk MCP Marketplace](https://mcp.dingtalk.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify DingTalk cloud documents and may export document content to local Markdown files.]

## Skill Version(s):

1.0.0 (source: release evidence; artifact package and changelog version 0.3.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
