## Description:

Generate videos through Filtrix Remote MCP for text-to-video, image-to-video, video task polling, and downloading completed videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lumenclaw-cloud](https://clawhub.ai/user/lumenclaw-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative operators use this skill to submit Filtrix MCP video generation jobs, poll their status, and download completed outputs from a command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials, prompts, and source images may be sent to a custom MCP endpoint if FILTRIX_MCP_URL is changed.

Mitigation: Use the default Filtrix MCP endpoint unless the custom endpoint is intentionally trusted, keep the API key scoped or disposable where possible, and avoid submitting sensitive prompts or images without reviewing Filtrix data handling.

Risk: Downloaded videos come from returned URLs that are not constrained or size-limited by the skill evidence.

Mitigation: Treat downloaded videos as untrusted files, download to a controlled path, avoid untrusted or test MCP endpoints, and scan files before opening or sharing them.

## Reference(s):

- [MCP Tools Reference](references/mcp-tools.md)
- [Video Prompt Guide](references/prompts.md)
- [Filtrix MCP Endpoint](https://mcp.filtrix.ai/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with inline bash commands, optional JSON status output, and optional downloaded video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FILTRIX_MCP_API_KEY and may use FILTRIX_MCP_URL to target a custom MCP endpoint.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
