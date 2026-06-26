## Description: <br>
Query AdGuard Home instances for real-time DNS stats, blocked domains, client activity, service status, and configuration details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[foxleoly](https://clawhub.ai/user/foxleoly) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and self-hosted infrastructure users use this skill to inspect AdGuard Home DNS activity, blocking behavior, client usage, service health, and configuration from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AdGuard credentials can be exposed if stored in a shared or world-readable local configuration file. <br>
Mitigation: Prefer environment variables or a secrets manager, and set any local adguard-instances.json file to owner-only permissions. <br>
Risk: DNS query logs and client activity can reveal browsing behavior and internal network details. <br>
Mitigation: Avoid sharing query-log output and restrict skill use to users who are authorized to view AdGuard monitoring data. <br>
Risk: Using overly broad AdGuard credentials can expose more account capability than the monitoring workflow needs. <br>
Mitigation: Use the least-privileged AdGuard account available for the monitored instances. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/foxleoly/adguard-test) <br>
- [README](artifact/README.md) <br>
- [Security Audit](artifact/SECURITY_AUDIT.md) <br>
- [Test Report](artifact/TEST_REPORT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text command output with setup guidance and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include DNS query logs, client activity, blocked domains, service status, and configuration details from configured AdGuard Home instances.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
