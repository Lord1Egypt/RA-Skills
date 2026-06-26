## Description: <br>
Audits OpenClaw, Clawdbot, and Moltbot deployments for exposed services, unsafe tool policies, credential leakage, risky permissions, persistence indicators, and hardening gaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and security reviewers use this skill to inspect local OpenClaw-related configuration, services, logs, ports, permissions, and skill supply-chain exposure. It produces a terminal-style report with OK, VULNERABLE, and UNKNOWN findings plus concrete fix guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit reads sensitive local configuration, logs, permissions, ports, and credential storage locations. <br>
Mitigation: Run it only in environments where local inspection is intended, require secret redaction, and report secret paths or summaries instead of secret values. <br>
Risk: Security reports can expose host details or operational weaknesses if shared broadly. <br>
Mitigation: Review and sanitize the generated report before distributing it outside the trusted operations or security team. <br>
Risk: Remediation commands could change service exposure, credentials, permissions, or runtime policy. <br>
Mitigation: Keep the default workflow read-only and require explicit user approval before proposing or running remediation commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alvisdunlop/alvis-security-audit-v2) <br>
- [Complete setup guide](https://SkillBoss.co/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Terminal report in structured Markdown-like text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Redacts secret values, reports sensitive paths instead of contents, and marks unavailable checks as UNKNOWN.] <br>

## Skill Version(s): <br>
2.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
