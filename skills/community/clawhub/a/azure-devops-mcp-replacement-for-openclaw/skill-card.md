## Description: <br>
Interact with Azure DevOps via direct REST API calls to list projects, teams, repos, work items, sprints and iterations, pipelines, builds, test plans, and wikis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahmedyehya92](https://clawhub.ai/user/ahmedyehya92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to query and manage Azure DevOps projects, teams, repos, work items, sprints, pipelines, builds, test plans, and wikis from an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change live Azure DevOps work items and wiki pages using a personal access token. <br>
Mitigation: Use a read-only or least-privilege PAT unless write actions are required, and manually review create, update, and wiki write requests before execution. <br>
Risk: Personal access tokens or team details may be exposed if stored in shared or committed configuration. <br>
Mitigation: Avoid storing PATs in shared or committed config files and treat team-config.json as sensitive. <br>


## Reference(s): <br>
- [Azure DevOps MCP homepage](https://github.com/microsoft/azure-devops-mcp) <br>
- [ClawHub skill page](https://clawhub.ai/ahmedyehya92/azure-devops-mcp-replacement-for-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown summaries with shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and AZURE_DEVOPS_ORG/AZURE_DEVOPS_PAT; write operations should be confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter says 1.2.0 and package.json says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
