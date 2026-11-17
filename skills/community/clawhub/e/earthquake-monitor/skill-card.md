## Description:

Real-time earthquake monitoring for China, Taiwan, and Japan using CENC, CWA, and JMA data with configurable proactive alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fungjcode](https://clawhub.ai/user/fungjcode)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to query recent earthquake activity, configure monitored locations, and receive distance- and magnitude-based alerts for China, Taiwan, and Japan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook URLs may be stored in plaintext local configuration.

Mitigation: Avoid storing token-bearing webhook URLs unless local file permissions and operational controls are acceptable.

Risk: Earthquake alerts depend on third-party aggregator endpoints and may overstate source reliability.

Mitigation: Treat alerts as advisory and verify critical events against authoritative government or emergency-management channels.

Risk: Network polling and local configuration writes are expected behavior.

Mitigation: Review network access and local write permissions before installing in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fungjcode/skills/earthquake-monitor)
- [Publisher profile](https://clawhub.ai/user/fungjcode)
- [Security policy](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Configuration, Guidance]

**Output Format:** [JavaScript-returned objects and human-readable alert messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include earthquake lists, alert status, localized alert text, city configuration, and monitoring status.]

## Skill Version(s):

1.1.1 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
