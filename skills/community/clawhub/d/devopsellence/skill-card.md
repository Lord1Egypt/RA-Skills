## Description: <br>
Operate devopsellence solo/shared deployments, nodes, secrets, logs, diagnostics, lifecycle hooks, and rollback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elvinefendi](https://clawhub.ai/user/elvinefendi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to deploy applications with devopsellence, choose solo or shared workspace modes, manage secrets and nodes, inspect logs and diagnostics, and handle lifecycle-hook configuration and rollback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Node cleanup and management actions can detach, uninstall, or remove deployment infrastructure. <br>
Mitigation: Require the agent to show the target node, environment, and likely impact, then get explicit confirmation before detach, uninstall, remove, --yes, provider-token, SSH-key, or production-secret actions. <br>


## Reference(s): <br>
- [devopsellence homepage](https://www.devopsellence.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses structured CLI output where available and advises keeping secrets out of logs and chat output.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
