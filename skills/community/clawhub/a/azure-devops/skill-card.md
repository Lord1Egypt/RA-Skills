## Description: <br>
List Azure DevOps projects, repositories, and branches; create pull requests; manage work items; check build status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PALs-Software](https://clawhub.ai/user/PALs-Software) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to inspect Azure DevOps projects, repositories, branches, pull requests, work items, and build status, and to prepare Azure DevOps REST API commands for common workflow actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses and may store an Azure DevOps Personal Access Token, which is a sensitive credential. <br>
Mitigation: Use a dedicated least-privilege PAT limited to the required organization, projects, and actions, and remove stored credentials when no longer needed. <br>
Risk: Some generated commands can create or change Azure DevOps resources, including pull requests and work items. <br>
Mitigation: Manually review and confirm any command that creates or changes Azure DevOps resources before execution. <br>


## Reference(s): <br>
- [Azure DevOps REST API documentation](https://learn.microsoft.com/en-us/rest/api/azure/devops/) <br>
- [ClawHub Azure DevOps skill page](https://clawhub.ai/PALs-Software/azure-devops) <br>
- [PALs-Software publisher profile](https://clawhub.ai/user/PALs-Software) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, AZURE_DEVOPS_PAT, and an Azure DevOps organization name.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
