## Description: <br>
Doctor Check helps diagnose OpenClaw and runtime environment health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soroyue](https://clawhub.ai/user/soroyue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run local OpenClaw diagnostics covering environment readiness, service state, configuration health, and recent log issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect sensitive local configuration, API-key validity, service state, and logs without clear scope or redaction rules. <br>
Mitigation: Define permitted config files, services, and log paths before use, require secrets and tokens to be redacted, and approve file cleanup or credential validation separately. <br>


## Reference(s): <br>
- [Doctor Check on ClawHub](https://clawhub.ai/soroyue/doctor-check) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown diagnostic report with categorized normal, warning, and problem findings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local health observations about services, configuration, API-key validity, permissions, disk space, and logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
