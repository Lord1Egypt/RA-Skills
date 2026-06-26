## Description: <br>
Automatically audits newly installed skills to validate structure, security, and health before activation, preventing broken or malicious skills from running. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yoborlon-alpha](https://clawhub.ai/user/yoborlon-alpha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to audit newly installed OpenClaw skills before activation, checking structure, obvious secret patterns, file permissions, and basic health. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A PASS result could be mistaken for complete security approval of an untrusted skill. <br>
Mitigation: Use the audit as a lightweight local checklist and continue to review untrusted skills before enabling them. <br>
Risk: Running the audit against the wrong directory can produce irrelevant or misleading results. <br>
Mitigation: Run it against the exact skill directory intended for activation. <br>


## Reference(s): <br>
- [Skill Audit on ClawHub](https://clawhub.ai/yoborlon-alpha/claw-skill-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text with PASS, WARN, FAIL, and INFO status lines plus an exit code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local skill directory path; a PASS result is not a complete security approval for untrusted skills.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
