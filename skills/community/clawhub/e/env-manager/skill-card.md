## Description: <br>
Manage environment variables, secrets, and configuration across agent sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imaflytok](https://clawhub.ai/user/imaflytok) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers can use this skill for local environment profile setup, credential rotation checks, and agent-session configuration guidance. Use it as low-risk local convenience guidance and review secret handling before using it with production credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documentation may overstate secret protection by describing plaintext file storage and chmod permissions as encryption. <br>
Mitigation: Treat generated secret and environment files as plaintext unless an independently verified encryption mechanism is added; restrict file permissions and use a dedicated secret manager for sensitive credentials. <br>
Risk: Plaintext environment files and sourced production profiles can expose secrets through backups, logs, shell history, process environments, or local compromise. <br>
Mitigation: Load production credentials only for the specific command that needs them, avoid logging environment values, and keep production profiles out of broad session startup hooks. <br>
Risk: The third-party credential sharing suggestion may introduce trust and data exposure risk. <br>
Mitigation: Do not use the suggested sharing service for real credentials unless the operator independently trusts and understands that service. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/imaflytok/env-manager) <br>
- [ClawSwarm](https://onlyflies.buzz/clawswarm/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local environment management guidance; it does not provide a verified encryption implementation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
