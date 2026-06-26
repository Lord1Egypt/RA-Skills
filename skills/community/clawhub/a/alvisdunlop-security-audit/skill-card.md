## Description: <br>
Audits OpenClaw, Clawdbot, and Moltbot deployments for misconfigurations and attack vectors, including gateway exposure, skill safety, credential leakage, and hardening gaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and security reviewers use this skill to perform read-only audits of OpenClaw, Clawdbot, and Moltbot environments. It helps identify exposed gateways or control UIs, unsafe tool policies, credential storage issues, untrusted skills, and privilege or persistence risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local audit output may include sensitive environment details or paths related to credentials and services. <br>
Mitigation: Run the skill only on systems you control, review the report before sharing it, and redact secrets or sensitive host details. <br>
Risk: Remediation actions can change security settings, rotate keys, stop processes, or alter configuration. <br>
Mitigation: Keep the audit read-only by default and require explicit confirmation before running any remediation command. <br>
Risk: Some checks may require elevated access and could expose more system information than necessary. <br>
Mitigation: Avoid unnecessary root access and use the least privilege needed to collect evidence. <br>


## Reference(s): <br>
- [Security Audit ClawHub page](https://clawhub.ai/alvisdunlop/alvisdunlop-security-audit) <br>
- [Complete setup guide](https://SkillBoss.co/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown-style terminal report with check IDs, statuses, evidence summaries, impact, fixes, and a final summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings use OK, VULNERABLE, or UNKNOWN status labels; remediation commands are proposed only after explicit user approval.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
