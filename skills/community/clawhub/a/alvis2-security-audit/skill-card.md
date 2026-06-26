## Description: <br>
Audit OpenClaw/Clawdbot deployments for misconfigurations and attack vectors, including gateway/control UI exposure, skill safety, credential leakage, and hardening guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to perform a read-only security review of OpenClaw, Clawdbot, or Moltbot deployments and produce actionable findings with remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit may inspect sensitive local paths such as logs, environment files, and OpenClaw configuration directories. <br>
Mitigation: Keep outputs local, report paths or summaries instead of secret values, and verify that any detected secrets are redacted before sharing results. <br>
Risk: The skill can propose remediation commands after finding vulnerable configuration. <br>
Mitigation: Review each remediation command and approve only commands that match the intended change. <br>
Risk: Broad read-only system inspection can expose host, process, network, or service details in the report. <br>
Mitigation: Limit report distribution to trusted recipients and remove environment-specific details that are not needed for the review. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/alvisdunlop/alvis2-security-audit) <br>
- [SkillBoss Setup Guide](https://SkillBoss.co/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style terminal report with OK, VULNERABLE, and UNKNOWN findings, evidence summaries, impact notes, and fixes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only audit posture by default; remediation commands are proposed only after explicit user approval.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
