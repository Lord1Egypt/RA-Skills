## Description: <br>
Check deployment status of PRs and commits using continuous-deployment MCP and UCS deployer MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajitsingh25](https://clawhub.ai/user/ajitsingh25) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to check whether a GitHub PR, commit, or recent service commit has reached staging or production through continuous-deployment and UCS deployment systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to query internal PR and deployment-status data. <br>
Mitigation: Install and use it only where the agent is authorized to read that data, and provide a specific PR, commit, service, or environment to keep lookups scoped. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ajitsingh25/check-deployment-status) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands] <br>
**Output Format:** [Markdown with command examples and MCP tool-call parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only deployment-status guidance scoped to the PR, commit, service, or environment the user provides.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
