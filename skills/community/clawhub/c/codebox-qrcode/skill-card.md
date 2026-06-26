## Description: <br>
Generate, manage, and track QR codes via the CodeBox API, including dynamic QR codes, style templates, scan analytics, batch generation, and lifecycle actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gdfsdjj145](https://clawhub.ai/user/gdfsdjj145) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create styled QR codes, manage dynamic QR destinations, inspect scan analytics, and export scan events through CodeBox. It is suited for QR campaigns where the user has a CodeBox API key and accepts CodeBox credit and tracking behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scan analytics and exported scan events can include device, location, and time data. <br>
Mitigation: Collect and export only the analytics needed for the task, obtain consent where required, and avoid sharing unnecessary scan data. <br>
Risk: Deleting or changing dynamic QR codes can disrupt live QR campaigns or redirect users to the wrong destination. <br>
Mitigation: Confirm the QR code ID, target URL, and campaign impact before update or delete actions, especially for live campaigns. <br>
Risk: Dynamic QR generation consumes CodeBox credits. <br>
Mitigation: Use static QR codes when tracking is not needed and batch generation only after confirming the requested list. <br>


## Reference(s): <br>
- [CodeBox website](https://www.codebox.club) <br>
- [CodeBox API docs](https://www.codebox.club/docs/api) <br>
- [CodeBox API Reference](references/api.md) <br>
- [CodeBox SDK](https://www.codebox.club/docs/sdk) <br>
- [CodeBox MCP server](https://www.codebox.club/docs/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/gdfsdjj145/codebox-qrcode) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown with curl commands and JSON request or response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CODEBOX_API_KEY and curl for API-backed actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
