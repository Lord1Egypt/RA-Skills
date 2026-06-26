## Description: <br>
Display, set, and manage environment variables in shell sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect environment variables in a shell session, including checking whether specific variables are set and reviewing the runtime environment for debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Listing all environment variables can expose API keys, tokens, passwords, cloud credentials, or internal endpoints. <br>
Mitigation: Query only specific non-sensitive variables when possible and avoid running full environment dumps in shells that may contain secrets. <br>


## Reference(s): <br>
- [Env Tool on ClawHub](https://clawhub.ai/dinghaibin/env-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text environment-variable output with optional markdown shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May print sensitive environment values when listing all variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
