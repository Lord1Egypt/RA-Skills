## Description: <br>
Security Audit helps agents audit OpenClaw, Clawdbot, and Moltbot deployments for misconfigurations, public exposure, unsafe tool policies, credential leakage, and hardening gaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run read-only OpenClaw and Clawdbot security reviews. It produces a terminal audit report with findings, evidence, impact, and fix guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects local host, network, process, log, and credential-storage state, so its report may contain sensitive system details or secret paths. <br>
Mitigation: Run checks read-only, redact secret values, and review the generated report before sharing it. <br>
Risk: The artifact references an external setup guide that is outside the server-resolved provenance. <br>
Mitigation: Inspect the external guide separately before following it. <br>


## Reference(s): <br>
- [Security Audit on ClawHub](https://clawhub.ai/alvisdunlop/alvis-sec-audit) <br>
- [Publisher profile](https://clawhub.ai/user/alvisdunlop) <br>
- [Complete setup guide](https://SkillBoss.co/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal report with status sections, evidence summaries, impact notes, and fix guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Secret values should be redacted; remediation commands are proposed only when the user explicitly requests them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
