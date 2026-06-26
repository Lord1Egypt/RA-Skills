## Description: <br>
Atlassian Bitbucket Cloud skill for full CRUD automation across repositories, pull requests, pipelines, issues, snippets, workspaces, branches, deployments, and related Bitbucket REST API 2.0 resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abdelkrim](https://clawhub.ai/user/abdelkrim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to inspect and automate Bitbucket Cloud repositories, pull requests, pipelines, issues, workspace resources, and related configuration from an agent-assisted workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Bitbucket credentials can give the skill access beyond the intended workflow. <br>
Mitigation: Use a dedicated Atlassian API token with only the scopes needed for the planned commands. <br>
Risk: Repository, pipeline, issue, key, variable, or workspace changes can affect production Bitbucket resources. <br>
Mitigation: Review proposed commands before execution and reserve destructive operations for cases where the required confirmation flag is intentional. <br>
Risk: Secrets can be exposed if pasted into shared shells, logs, or agent transcripts. <br>
Mitigation: Provide credentials through environment variables or other safer secret-handling paths instead of pasting real tokens into command history. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/abdelkrim/atlassian-bitbucket-by-altf1be) <br>
- [Bitbucket REST API documentation](https://developer.atlassian.com/cloud/bitbucket/rest/intro/) <br>
- [Atlassian API token setup](https://id.atlassian.com/manage-profile/security/api-tokens) <br>
- [API coverage](docs/API-COVERAGE.md) <br>
- [Bitbucket endpoint reference](references/bitbucket-endpoints.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Bitbucket credentials through environment variables; destructive commands require explicit confirmation.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
