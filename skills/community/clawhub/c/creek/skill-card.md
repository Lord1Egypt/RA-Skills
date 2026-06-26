## Description: <br>
Deploy and manage applications on Creek via the Creek CLI, including initialization, deployments, status checks, project and deployment history, rollbacks, environment variables, custom domains, and development server workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linyiru](https://clawhub.ai/user/linyiru) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to operate Creek deployments from an agent, including authentication, project setup, deployment, rollback, environment-variable management, and custom-domain management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through live deployment, rollback, domain, and environment-variable operations. <br>
Mitigation: Require explicit user approval before commands that deploy, rollback, modify domains, or change environment variables. <br>
Risk: The skill documents token-based authentication and commands that can reveal environment-variable values. <br>
Mitigation: Use a limited-scope Creek token and avoid showing environment-variable values unless the user explicitly needs them. <br>
Risk: The artifact encourages `--yes`, which can skip confirmation prompts. <br>
Mitigation: Do not use skipped confirmations for destructive or account-affecting operations unless the user has approved the exact action. <br>


## Reference(s): <br>
- [Creek skill page](https://clawhub.ai/linyiru/creek) <br>
- [Publisher profile](https://clawhub.ai/user/linyiru) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Creek CLI JSON output and breadcrumb fields to guide follow-up commands.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
