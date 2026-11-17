## Description:

Accessibility testing and remediation using the axe MCP Server for web pages and UI code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dylanb](https://clawhub.ai/user/dylanb)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to scan live or local web pages for accessibility violations and request remediation guidance while creating or modifying UI code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned Docker image and passes AXE_API_KEY into the container.

Mitigation: Use a digest-pinned image, restrict Docker access, and rotate the Axe API key if command logging or Docker inspection may expose it.

Risk: Tested page URLs, HTML snippets, and remediation text may be sent to the Axe MCP service.

Mitigation: Scan only approved content and avoid sensitive internal pages unless that use is explicitly approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dylanb/skills/axe-devtools)
- [Deque axe MCP Server](https://www.deque.com/axe/mcp-server/)
- [Deque support portal](https://support.deque.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON-RPC scan output, and code fix suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analyze output contains violation data; remediation output can include general_description, remediation, and code_fix fields.]

## Skill Version(s):

4.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
