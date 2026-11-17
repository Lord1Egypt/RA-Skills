## Description:

Interact with Azure DevOps through direct REST API calls to list projects, teams, repos, work items, sprints and iterations, pipelines, builds, test plans, and wikis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmedyehya92](https://clawhub.ai/user/ahmedyehya92)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to query Azure DevOps organization data, inspect agile delivery state, and perform selected work item or wiki updates from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an Azure DevOps PAT that can expose broad organization data and may permit modifications depending on token scopes.

Mitigation: Use the narrowest PAT scopes that support the intended workflow and avoid automatic use on vague Azure DevOps requests.

Risk: The skill includes create or update actions for work items and wiki pages.

Mitigation: Review proposed create, update, and wiki write actions before execution, especially when the request is ambiguous.

Risk: Team tracking can involve employee emails, sprint assignments, estimates, and capacity data stored in team-config.json.

Mitigation: Protect team-config.json and avoid sharing generated standup or capacity output beyond the intended team context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ahmedyehya92/skills/azure-devops-mcp-replacement-for-openclaw)
- [Azure DevOps MCP homepage from ClawHub metadata](https://github.com/microsoft/azure-devops-mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Azure DevOps organization and PAT environment configuration; output can include organization, project, work item, sprint, repository, pipeline, build, wiki, test plan, and team workload data.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.2.0 and package.json says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
