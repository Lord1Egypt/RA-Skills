## Description: <br>
Automate Brevo (Sendinblue) tasks via Rube MCP (Composio): manage email campaigns, create/edit templates, track senders, and monitor campaign performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sohamganatra](https://clawhub.ai/user/sohamganatra) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and marketing operators use this skill to guide agents through Brevo email campaign, template, sender, and A/B testing workflows via an authenticated Rube MCP connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Template deletion can remove Brevo account assets if the agent acts on the wrong template. <br>
Mitigation: List or fetch the exact template first, confirm the template ID and name with the user, and proceed only after explicit confirmation. <br>
Risk: Campaign and template updates may use stale or incorrect MCP schemas. <br>
Mitigation: Search Rube tools before each workflow and use the current returned schema for parameters. <br>


## Reference(s): <br>
- [Brevo Automation on ClawHub](https://clawhub.ai/sohamganatra/brevo-automation) <br>
- [Rube MCP server](https://rube.app/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, API Calls] <br>
**Output Format:** [Markdown guidance with MCP tool names, parameters, workflow steps, and operational cautions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an active Rube MCP connection and an authenticated Brevo account.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
