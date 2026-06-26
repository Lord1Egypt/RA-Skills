## Description: <br>
Security-focused PowerShell specialist skilled in hardening Windows systems, securing automation, enforcing least privilege, and aligning scripts with enterprise security baselines and compliance frameworks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtsatryan](https://clawhub.ai/user/mtsatryan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, Windows administrators, and security engineers use this skill to review and improve PowerShell usage, endpoint hardening, remoting controls, credential handling, logging, and automation security. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Privileged Windows hardening changes can disrupt remoting, firewall access, service accounts, credential storage, or local administrator access if applied to the wrong systems. <br>
Mitigation: Request audit or report mode first, confirm the target machines and administrator privileges, and keep rollback steps before applying generated commands. <br>
Risk: PowerShell automation guidance can mishandle credentials or expose sensitive output if adapted without review. <br>
Mitigation: Review scripts and commands for plaintext credentials, secure storage, sanitized logging, and least-privilege behavior before use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional PowerShell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands and configuration changes should be reviewed before privileged execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
