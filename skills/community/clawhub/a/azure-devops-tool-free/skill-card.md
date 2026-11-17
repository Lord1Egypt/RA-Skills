## Description:

Azure DevOps 基础版 helps agents manage Azure DevOps projects, repositories, branches, pull requests, and work item lookup for individual developer workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and individual Azure DevOps users use this skill to inspect organizations, projects, repositories, and branches, then create or review pull requests through an agent using Azure DevOps credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a Personal Access Token to make live Azure DevOps repository changes, including pull request creation.

Mitigation: Use the narrowest PAT scopes possible and review the organization, project, repository, branch, and pull request payload before execution.

Risk: The artifact includes a local-only privacy claim, but authenticated requests are sent to Azure DevOps for normal operation.

Mitigation: Treat Azure DevOps API calls as external network activity and avoid exposing tokens or sensitive project data in prompts, logs, or shared outputs.

Risk: The security evidence describes the instructions as misleading or overbroad.

Mitigation: Have the agent propose commands and API calls for review before running them, especially for write operations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/azure-devops-tool-free)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and structured Azure DevOps operation results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide authenticated Azure DevOps REST API calls using a user-provided PAT.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
