## Description: <br>
Connect and use Fantopy's MCP server for World Cup 2026 predictions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fantopy](https://clawhub.ai/user/fantopy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an MCP-capable agent to Fantopy's free-to-play World Cup prediction game, browse fixtures, make confirmed score predictions, manage groups, and share public watch links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent could save score predictions before the user has confirmed the exact fixtures and scores. <br>
Mitigation: Repeat the exact picks and ask for confirmation before calling prediction-saving tools. <br>
Risk: Public handles, watch links, email login codes, and recovery codes can expose account-related information. <br>
Mitigation: Treat these values as account-related information, keep recovery codes private, and avoid sharing login codes or recovery codes in public contexts. <br>
Risk: Hosted MCP sessions configured without OAuth can create a fresh anonymous player for each session, and unsaved anonymous progress may be unrecoverable. <br>
Mitigation: Configure the hosted MCP service with OAuth and offer email login or a recovery code after the user makes meaningful progress. <br>


## Reference(s): <br>
- [Fantopy MCP ClawHub listing](https://clawhub.ai/fantopy/fantopy-mcp) <br>
- [Fantopy MCP homepage](https://github.com/Fantopy-ai/fantopy-mcp) <br>
- [Fantopy hosted MCP endpoint](https://mcp.fantopy.ai/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an MCP-capable client and OAuth for the hosted Fantopy MCP service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
