## Description: <br>
Triggers Jenkins CI or deployment jobs for selected repositories and sends a Feishu build or deployment notification after successful completion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunyang777](https://clawhub.ai/user/sunyang777) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Release engineers and developers use this skill when they explicitly want an agent to trigger configured Jenkins CI/CD jobs, wait for completion, and notify Feishu recipients about package or deployment status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence says this version ships hardcoded CI/CD and Feishu credentials that could allow unintended build, deployment, or notification actions. <br>
Mitigation: Do not install unless the publisher is fully trusted; rotate the exposed Jenkins, Feishu, and GitHub credentials and move secrets to a secure runtime source before routine use. <br>
Risk: The skill can trigger Jenkins jobs and send Feishu notifications against configured external systems. <br>
Mitigation: Grant access only in environments where these Jenkins and Feishu operations are intended, and require explicit user requests with complete repository, branch, and change details before invocation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunyang777/ci-package-deploy-notify) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs Jenkins and Feishu network operations through bundled Python scripts when invoked.] <br>

## Skill Version(s): <br>
1.0.7 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
