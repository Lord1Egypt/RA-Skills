## Description: <br>
Domain Research Tool helps agents run domain research across RDAP, WHOIS, DNS records, SSL/TLS certificates, domain availability, reverse DNS, multi-resolver checks, subdomain enumeration, batch analysis, and interactive HTML reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security teams, and operations teams use this skill to research domains, inspect registration, DNS, and SSL signals, assess availability, run authorized batch or subdomain checks, and produce structured reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound domain-research requests to registries, WHOIS and DNS infrastructure, public resolvers, target HTTPS endpoints, and common subdomains. <br>
Mitigation: Run batch and subdomain checks only for domains you are authorized to assess and expect the listed outbound lookups when invoking the skill. <br>
Risk: Generated HTML reports contain third-party lookup data. <br>
Mitigation: Open generated reports cautiously and review their contents before sharing or using them in sensitive workflows. <br>
Risk: RDAP, WHOIS, DNS, and SSL results can be incomplete, cached, unavailable, rate limited, or inconsistent across registries and resolvers. <br>
Mitigation: Treat findings as research signals and corroborate important decisions with authoritative registries, DNS providers, or certificate sources. <br>


## Reference(s): <br>
- [Domain Research Protocols Reference](references/domain_protocols.md) <br>
- [IANA RDAP Bootstrap](https://data.iana.org/rdap/) <br>
- [ClawHub Domain Research Tool Release](https://clawhub.ai/bettermen/domain-research) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell commands; lookup results are JSON or text, with optional self-contained HTML reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write JSON result files and HTML reports; batch mode accepts one domain per line.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
