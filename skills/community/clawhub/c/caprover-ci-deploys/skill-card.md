## Description: <br>
Deploy apps to CapRover and set up GitHub Actions CI/CD workflows for new or existing projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guim4dev](https://clawhub.ai/user/guim4dev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to trigger CapRover deployments, check deployment status, and scaffold GitHub Actions workflows and CapRover deployment files for application projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger real GitHub Actions and CapRover deployments using stored credentials. <br>
Mitigation: Require manual confirmation of the app, repository, branch, environment, and deploy strategy before any live deployment. <br>
Risk: Credential exposure or overly broad credentials could expand deployment access. <br>
Mitigation: Protect config.json, prefer per-app CapRover tokens or webhook URLs over a master password, and use a least-privilege GitHub token. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/guim4dev/caprover-ci-deploys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, YAML workflow templates, JSON configuration examples, and deployment status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can trigger GitHub Actions workflow dispatches, CapRover webhooks, or CapRover CLI deploys when configured with credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
