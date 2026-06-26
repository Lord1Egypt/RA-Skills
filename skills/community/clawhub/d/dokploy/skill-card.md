## Description: <br>
Manage Dokploy deployments, projects, applications, and domains via the Dokploy API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JoshuaRileyDev](https://clawhub.ai/user/JoshuaRileyDev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to manage Dokploy projects, applications, deployments, domains, and environment variables from an agent-assisted command-line workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dokploy API keys can grant deployment-management authority and may be persisted in local configuration. <br>
Mitigation: Use the narrowest API key possible, prefer environment variables for sensitive credentials, and protect or remove local config files that store keys. <br>
Risk: Environment variable listings, deployment logs, and config output may expose application secrets. <br>
Mitigation: Review output before sharing it, redact sensitive values, and avoid running secret-bearing commands in public or shared sessions. <br>
Risk: Deployment, environment, domain, and delete commands can change live Dokploy resources. <br>
Mitigation: Review every generated command and its target IDs before execution, especially destructive or production-impacting operations. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; uses Dokploy API credentials supplied by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: .clawdhub/package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
