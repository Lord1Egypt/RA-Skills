## Description: <br>
Query AdGuard Home instances for real-time DNS stats, blocked domains, client activity, service status, configs, filter rules, and recent query logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[foxleoly](https://clawhub.ai/user/foxleoly) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and self-hosted network administrators use this skill to inspect AdGuard Home DNS activity, blocking performance, service health, and configuration from an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles AdGuard Home administrative credentials. <br>
Mitigation: Prefer environment variables or a secrets manager; if using adguard-instances.json, keep it out of version control and restrict it to owner-only permissions. <br>
Risk: Query-log and client output can expose private browsing and network metadata. <br>
Mitigation: Install and use this only where the agent and user should have AdGuard administrative visibility, and avoid sharing outputs outside authorized contexts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/foxleoly/adguard-home) <br>
- [README](README.md) <br>
- [Security Audit](SECURITY_AUDIT.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Plain text command output with formatted status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Query-log output is bounded by a validated limit of 1 to 100 entries; operation requires configured AdGuard Home access.] <br>

## Skill Version(s): <br>
1.2.7 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
