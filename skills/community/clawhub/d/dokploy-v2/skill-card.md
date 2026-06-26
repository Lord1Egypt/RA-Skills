## Description: <br>
Manage Dokploy deployments, projects, applications, and domains via the Dokploy API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laoshu133](https://clawhub.ai/user/laoshu133) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to configure Dokploy API access and manage projects, applications, domains, deployments, deployment logs, and application environment variables from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Dokploy API credentials that may allow deployment, deletion, and environment-variable changes. <br>
Mitigation: Use a limited-scope API key where possible and require explicit approval before production deploy, delete, or environment-variable changes. <br>
Risk: The dokploy-config helper can store the API URL and API key in ~/.dokployrc. <br>
Mitigation: Avoid persistent config storage for sensitive keys unless the file is access-controlled and appropriate for the user environment. <br>
Risk: Environment variables and deployment logs can contain secret material. <br>
Mitigation: Treat command output, environment values, and logs as sensitive and avoid exposing them in shared transcripts or public artifacts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/laoshu133/dokploy-v2) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/laoshu133) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and text or JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq, plus Dokploy API URL and API key configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
