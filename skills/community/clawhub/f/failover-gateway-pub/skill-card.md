## Description: <br>
Set up an active-passive failover gateway for OpenClaw with a standby node that auto-promotes when the primary goes down and auto-demotes when it recovers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ember-claw](https://clawhub.ai/user/ember-claw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to deploy an active-passive OpenClaw standby gateway for high availability, disaster recovery, and redundant access when a primary instance fails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The persistent health monitor can promote a standby service and copy a secrets directory during failover. <br>
Mitigation: Review every command before deployment, avoid SECRETS_HOST unless it is required, and sync only narrowly scoped secrets with limited tokens and verified SSH host keys. <br>
Risk: Installer commands run on servers and include curl-to-shell patterns. <br>
Mitigation: Prefer verified or package-managed installers where possible, and review installer sources before execution. <br>
Risk: Failover behavior can affect production availability if enabled without testing. <br>
Mitigation: Test failover in a controlled maintenance window before enabling the monitor. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ember-claw/failover-gateway-pub) <br>
- [Publisher Profile](https://clawhub.ai/user/ember-claw) <br>
- [Tailscale](https://tailscale.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash, JSON, and systemd configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes an optional health-monitor shell script and deployment checklist.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
