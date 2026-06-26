## Description: <br>
Avoid common Ansible mistakes - YAML syntax traps, variable precedence, idempotence failures, and handler gotchas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill as a concise Ansible reference for avoiding common playbook mistakes around YAML syntax, variables, idempotence, handlers, privilege escalation, conditionals, loops, facts, and dry runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may apply Ansible commands or playbook changes to real infrastructure without sufficient review, including changes involving privilege escalation or vault passwords. <br>
Mitigation: Review generated or selected Ansible commands and playbook changes before execution, test against non-production inventory when possible, and handle vault or sudo passwords according to local credential-management policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/ansible) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown reference notes with inline Ansible commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the ansible binary on Linux or macOS when users apply the guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
