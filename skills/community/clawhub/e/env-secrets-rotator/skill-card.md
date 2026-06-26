## Description: <br>
Rotate and update secrets in environment files, generate Vault commands, and manage secret rotation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Derick001](https://clawhub.ai/user/Derick001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to rotate values in local .env files, preview changes, validate simple environment files, and produce HashiCorp Vault CLI commands for manual secret-manager updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says rotated secret values can be stored in a plaintext home-directory history file. <br>
Mitigation: Start with --dry-run, avoid production secrets until rollout is planned, and delete or protect ~/.env-rotation-history.json after use. <br>
Risk: Backups of .env files may retain live plaintext credentials after rotation. <br>
Mitigation: Restrict access to generated backup files and delete them after confirming the rotation succeeded. <br>
Risk: The tool only generates Vault CLI commands and does not update remote secret managers itself. <br>
Mitigation: Review the generated commands, replace placeholders where needed, and run them through an approved secret-management workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Derick001/env-secrets-rotator) <br>
- [Publisher profile](https://clawhub.ai/user/Derick001) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Files, Configuration guidance] <br>
**Output Format:** [JSON results, human-readable summaries, updated .env files, backups, and HashiCorp Vault CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated secrets and backup/history files may contain plaintext credential material.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
