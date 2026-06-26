## Description: <br>
Claw Gatekeeper is a persistent OpenClaw security layer that assesses operation risk, prompts for human approval on higher-risk actions, and records audit logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stephenlzc](https://clawhub.ai/user/stephenlzc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add human-in-the-loop controls around file, shell, network, skill installation, and configuration operations so higher-risk actions are reviewed before proceeding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the promised protections do not fully match the defaults, examples, and installation guidance. <br>
Mitigation: Review the effective configuration after installation and use strict or hardened mode when MEDIUM actions should require confirmation. <br>
Risk: The security guidance flags the README's curl-latest installation flow as a concern. <br>
Mitigation: Prefer a pinned ClawHub package or another verified, version-specific release source before installing. <br>
Risk: Session approvals, whitelists, audit logs, backups, and cleanup behavior affect how much protection the skill actually provides. <br>
Mitigation: Verify CRITICAL operations cannot be persistently allowed in the target setup and confirm where approvals, logs, backups, and cleanup jobs are stored. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/stephenlzc/claw-gatekeeper) <br>
- [Publisher Profile](https://clawhub.ai/user/stephenlzc) <br>
- [Security Deployment Guide](SECURITY.md) <br>
- [Claw-Gatekeeper Risk Matrix](references/risk_matrix.md) <br>
- [Claw-Gatekeeper User Guide](references/user_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and script references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for human review before security-sensitive operations.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
