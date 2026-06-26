## Description: <br>
Automate Canva tasks via Rube MCP (Composio): designs, exports, folders, brand templates, autofill. Always search tools first for current schemas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sohamganatra](https://clawhub.ai/user/sohamganatra) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to guide agents through Canva workflows such as listing designs, creating designs, uploading assets, exporting files, organizing folders, and autofilling brand templates through Rube MCP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides an agent to operate on Canva content through an external Rube MCP connection. <br>
Mitigation: Install and use it only when that external connection is intended and the Canva account has appropriate access for the task. <br>
Risk: Asset URLs shared during uploads may expose private, internal, signed, or otherwise sensitive content to Canva or Rube. <br>
Mitigation: Provide only asset URLs that are approved for sharing through the Canva/Rube workflow. <br>
Risk: Generated Canva export download links can expose exported design content while they remain valid. <br>
Mitigation: Treat export links as secrets and share or store them only in approved locations. <br>


## Reference(s): <br>
- [Rube MCP endpoint](https://rube.app/mcp) <br>
- [Canva Automation on ClawHub](https://clawhub.ai/sohamganatra/canva-automation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with tool sequences, parameter notes, and workflow cautions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may result in third-party Canva and Rube MCP operations when followed by an agent with the required connection.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
