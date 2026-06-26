## Description: <br>
Parse, interpret, and analyze Cisco ASA (Adaptive Security Appliance) firewall syslog messages for firewall event analysis, security investigations, syslog protocol context, ASA message formats, and message ID categorization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gangtao](https://clawhub.ai/user/gangtao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, security analysts, and network engineers use this skill to parse Cisco ASA syslog lines, identify severity and message IDs, and look up message meaning or recommended action during firewall monitoring and incident investigation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ASA logs can contain internal IP addresses, usernames, VPN details, and security events. <br>
Mitigation: Share only log excerpts that are appropriate for the agent to analyze, and redact sensitive identifiers when full fidelity is not needed. <br>
Risk: The skill provides documentation-based interpretation and lookup guidance rather than authoritative device state. <br>
Mitigation: Confirm high-impact findings against Cisco documentation, device configuration, and operational telemetry before making production changes. <br>


## Reference(s): <br>
- [Cisco ASA Syslog Analysis Skill](SKILL.md) <br>
- [About Cisco Secure Firewall ASA](references/About Cisco Secure Firewall ASA.md) <br>
- [Messages Listed by Severity Level](references/Messages Listed by Severity Level.md) <br>
- [Syslog Messages 101001 to 199027](references/Syslog Messages 101001 to 199027.md) <br>
- [Syslog Messages 201002 to 219002](references/Syslog Messages 201002 to 219002.md) <br>
- [Syslog Messages 302003 to 342008](references/Syslog Messages 302003 to 342008.md) <br>
- [Syslog Messages 400000 to 450002](references/Syslog Messages 400000 to 450002.md) <br>
- [Syslog Messages 500001 to 520025](references/Syslog Messages 500001 to 520025.md) <br>
- [Syslog Messages 602101 to 622102](references/Syslog Messages 602101 to 622102.md) <br>
- [Syslog Messages 701001 to 714011](references/Syslog Messages 701001 to 714011.md) <br>
- [Syslog Messages 715001 to 721019](references/Syslog Messages 715001 to 721019.md) <br>
- [Syslog Messages 722001 to 776020](references/Syslog Messages 722001 to 776020.md) <br>
- [Syslog Messages 776201 to 8300006](references/Syslog Messages 776201 to 8300006.md) <br>
- [Official Cisco ASA Syslog Documentation](https://www.cisco.com/c/en/us/td/docs/security/asa/syslog/asa-syslog.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/gangtao/cisco-asa-syslog) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with inline regular expressions and structured analysis guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only reference aid; does not execute code or call external tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
