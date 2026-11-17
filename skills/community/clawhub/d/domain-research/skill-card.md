## Description:

Investigates domains with RDAP, WHOIS, DNS record lookup, SSL/TLS certificate checks, availability checks, multi-resolver DNS propagation checks, subdomain enumeration, batch analysis, and interactive HTML reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security analysts, and operations teams use this skill to collect domain registration, DNS, SSL/TLS, availability, resolver propagation, subdomain, and reverse-DNS information and turn results into structured JSON or an HTML report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may render untrusted domain data without escaping.

Mitigation: Treat generated reports from attacker-controlled or untrusted domains as unsafe until output escaping is fixed; open them only in a constrained environment.

Risk: Domain, DNS, RDAP, WHOIS, SSL, and resolver checks disclose queried targets to external services.

Mitigation: Use the skill only for domains or IPs you are authorized to investigate, and avoid sensitive unreleased or internal targets unless external disclosure is acceptable.

Risk: Dependency installation can introduce package supply-chain risk.

Mitigation: Install dependencies in an isolated environment with pinned versions from a trusted package index.

## Reference(s):

- [Domain Research Protocols Reference](references/domain_protocols.md)
- [ClawHub skill page](https://clawhub.ai/bettermen/skills/domain-research)
- [Publisher profile](https://clawhub.ai/user/bettermen)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; the bundled scripts produce JSON and self-contained HTML reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can process single domains, IP reverse lookups, selected query types, or batch domain files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
