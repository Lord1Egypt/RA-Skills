## Description: <br>
Elastolink Meeting Skills helps agents use Elastolink/Ideasprite MCP meeting tools to list meetings, inspect meeting details, check device status, and export meeting documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netkiller](https://clawhub.ai/user/netkiller) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents working with Elastolink meetings use this skill to authenticate to the Ideasprite MCP endpoint, retrieve meeting lists, status, and details, and export meeting records as Markdown or Office documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API tokens may be exposed or persisted in unsafe places. <br>
Mitigation: Use the skill only for explicit Elastolink requests, avoid pasting long-lived tokens into chat or command arguments, keep .env out of source control and backups, and prefer a safer secret store or per-session environment variable. <br>
Risk: The skill can access meeting lists, meeting content, and exported documents. <br>
Mitigation: Install only where that level of meeting data access is appropriate and only if the Elastolink/Ideasprite endpoint is trusted. <br>
Risk: Broad activation language may cause unintended meeting-service calls. <br>
Mitigation: Restrict activation to clear Elastolink or meeting-management requests before running commands. <br>


## Reference(s): <br>
- [MCP Tools Reference](references/mcp-tools.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/netkiller/elastolink) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown or JSON-backed text with shell command invocations and exported document files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Meeting exports may include Markdown or Office document content returned by the Elastolink/Ideasprite MCP service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
