## Description:

Print, scan, copy, and job control for the Epson WF-2250 and other network-attached Epson inkjets via MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[earlvanze](https://clawhub.ai/user/earlvanze)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect an agent to an Epson printer MCP server for printing, diagnostics, printer status, and spooler job management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured MCP endpoint could receive documents, raw print payloads, and printer job commands.

Mitigation: Use only a server you control, verify the MCP server source and Docker Compose configuration, and avoid sending sensitive documents unless the endpoint operator and access controls are understood.

Risk: Raw printing and spooler controls can cause unintended printer output or job cancellation.

Mitigation: Use a rotatable bearer token, limit access to trusted users, and review requests before enabling raw printing or job-control operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/earlvanze/skills/epson-mcp)
- [Configured MCP endpoint](https://cyber.talpa-stargazer.ts.net/epson/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and MCP tool guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger printer actions or return printer diagnostics, status summaries, and job-control results through the configured MCP server.]

## Skill Version(s):

0.2.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
