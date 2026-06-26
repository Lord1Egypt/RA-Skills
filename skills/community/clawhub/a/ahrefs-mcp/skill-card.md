## Description: <br>
Ahrefs MCP helps agents access Ahrefs SEO data for site analysis, keyword research, backlink and competitor insights, rank tracking, and technical SEO audits through an MCP connection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jonathan-sokol](https://clawhub.ai/user/jonathan-sokol) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External SEO practitioners, marketers, and developers use this skill to connect an AI client to Ahrefs MCP and request SEO analysis, keyword research, backlink review, rank tracking, site audits, and competitive intelligence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The AI client may query Ahrefs account data and consume API units after authorization. <br>
Mitigation: Review the Ahrefs OAuth consent screen, set API unit limits when available, monitor usage, and revoke the MCP key when it is no longer needed. <br>
Risk: The optional local MCP server path depends on an external Ahrefs repository and installation steps. <br>
Mitigation: Use the hosted MCP endpoint for normal setup, or review the external repository and install steps before running a local server. <br>


## Reference(s): <br>
- [Ahrefs MCP Capability Reference](references/capabilities.md) <br>
- [Ahrefs MCP Setup Guide](references/setup.md) <br>
- [Ahrefs MCP Workflow Patterns](references/workflows.md) <br>
- [Ahrefs MCP Streamable HTTP Endpoint](https://api.ahrefs.com/mcp/mcp) <br>
- [Ahrefs MCP Claude Desktop and Web Guide](https://docs.ahrefs.com/docs/mcp/reference/claude-desktop-web) <br>
- [Ahrefs API Limits and Consumption](https://docs.ahrefs.com/docs/api/reference/limits-consumption) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown responses with setup steps, SEO analysis summaries, tables, and recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require an Ahrefs Lite or higher account, OAuth authorization, and API usage limits depending on plan.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
