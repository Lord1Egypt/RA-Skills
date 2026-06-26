## Description: <br>
AWS expert powered by the AWS Knowledge MCP Server via mcporter, providing real-time access to AWS documentation, best practices, SOPs, and regional availability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[w0yne](https://clawhub.ai/user/w0yne) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud engineers, and architects use this skill to answer AWS service, architecture, deployment, troubleshooting, regional availability, cost optimization, security hardening, infrastructure-as-code, and Well-Architected questions with cited AWS documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries may include secrets, account identifiers, or private architecture details. <br>
Mitigation: Use only approved MCP endpoints for sensitive data and avoid sending secrets or private account details unless that endpoint is trusted for the data. <br>
Risk: The skill depends on the mcporter npm package and a configured aws-knowledge MCP server. <br>
Mitigation: Confirm the mcporter package and configured MCP server are trusted before installing or using the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/w0yne/aws-knowledge) <br>
- [AWS Query Patterns by Domain](references/query-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with cited documentation links and inline shell commands when tool calls are relevant] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses mcporter to call a configured aws-knowledge MCP server and should include source URLs for verification.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
