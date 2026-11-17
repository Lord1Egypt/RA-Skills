## Description:

Parse, interpret, and analyze Cisco ASA (Adaptive Security Appliance) firewall syslog messages for log analysis, event triage, and security investigations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gangtao](https://clawhub.ai/user/gangtao)

### License/Terms of Use:


## Use Case:

External developers, security engineers, and operations teams use this skill to interpret Cisco ASA syslog lines, extract severity and message ID fields, and consult message-range references during firewall event analysis or investigations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cisco ASA logs, configurations, support archives, and topology details can contain sensitive operational or identity data.

Mitigation: Sanitize logs, configurations, support archives, tokens, usernames, IP addresses, and topology details before sharing them externally.

Risk: Firewall configuration commands or Cisco TAC guidance can affect production network behavior if applied without review.

Mitigation: Have an administrator review firewall configuration commands before applying them.

## Reference(s):

- [Official Cisco ASA Syslog Documentation](https://www.cisco.com/c/en/us/td/docs/security/asa/syslog/asa-syslog.html)
- [About Cisco Secure Firewall ASA](references/About Cisco Secure Firewall ASA.md)
- [Messages Listed by Severity Level](references/Messages Listed by Severity Level.md)
- [Syslog Messages 101001 to 199027](references/Syslog Messages 101001 to 199027.md)
- [Syslog Messages 201002 to 219002](references/Syslog Messages 201002 to 219002.md)
- [Syslog Messages 302003 to 342008](references/Syslog Messages 302003 to 342008.md)
- [Syslog Messages 400000 to 450002](references/Syslog Messages 400000 to 450002.md)
- [Syslog Messages 500001 to 520025](references/Syslog Messages 500001 to 520025.md)
- [Syslog Messages 602101 to 622102](references/Syslog Messages 602101 to 622102.md)
- [Syslog Messages 701001 to 714011](references/Syslog Messages 701001 to 714011.md)
- [Syslog Messages 715001 to 721019](references/Syslog Messages 715001 to 721019.md)
- [Syslog Messages 722001 to 776020](references/Syslog Messages 722001 to 776020.md)
- [Syslog Messages 776201 to 8300006](references/Syslog Messages 776201 to 8300006.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with structured log analysis and inline regular expressions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation and reference guidance; no executable tool calls or API actions are defined.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
