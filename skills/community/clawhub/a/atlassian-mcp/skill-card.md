## Description: <br>
Run the Model Context Protocol (MCP) Atlassian server in Docker, enabling integration with Jira, Confluence, and other Atlassian products. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AtakanErmis](https://clawhub.ai/user/AtakanErmis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to start an Atlassian MCP server for querying Jira issues, searching Confluence, and interacting with Atlassian services from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a third-party Docker image with access to Atlassian credentials and selected Jira or Confluence data. <br>
Mitigation: Install only after reviewing and trusting the upstream image, and pin the image to a reviewed version or digest. <br>
Risk: Agent access can include Jira-changing actions such as create, update, delete, or project-management operations. <br>
Mitigation: Use a dedicated least-privilege Atlassian account or token and require explicit approval before write actions. <br>
Risk: Jira API tokens can be exposed through shell history or overly broad credential handling. <br>
Mitigation: Provide credentials through environment variables or a secure secret mechanism and avoid placing tokens directly in command history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AtakanErmis/atlassian-mcp) <br>
- [Atlassian API token settings](https://id.atlassian.com/manage-profile/security/api-tokens) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash commands and environment-variable guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Docker and Jira credentials supplied through environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
