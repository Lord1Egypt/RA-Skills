## Description:

Connects Contracko over MCP and organises contracts, types, parties, and folders. Use for onboarding, filing, workspace structure, or whenever Contracko comes up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[contracko](https://clawhub.ai/user/contracko)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, legal operations teams, and agents use this skill to connect to a Contracko workspace, organize contract folders, types, fields, and parties, and route import, review, and agreement creation tasks to related Contracko skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contract metadata, text, or documents may be shared with the AI provider and the Contracko MCP server during use.

Mitigation: Use OAuth where possible, review requested scopes, disable provider training for real contract work, and avoid pasting credentials into chat.

Risk: Folder, type, party, import, reminder, or bulk update actions can change a Contracko workspace.

Mitigation: Confirm the intended destination or batch before writes and read back changed state before reporting completion.

Risk: Tool discovery, scope limits, or unknown outcomes can make workspace state ambiguous.

Mitigation: Treat discovered schemas as authoritative, validate result shape, and reconcile state after any OUTCOME_UNKNOWN response before retrying.

## Reference(s):

- [Contracko Skill Page](https://clawhub.ai/contracko/skills/contracko)
- [Contracko MCP Endpoint](https://app.contracko.com/mcp)
- [Contracko MCP Tool Index](references/tool-index.md)
- [Contracko Workflows](references/workflows.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live MCP tool discovery and asks for confirmation before workspace mutations.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
