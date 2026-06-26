## Description: <br>
DomainKits helps agents check domain availability, search related domains, explore domain data, and assess pricing, safety, keyword value, and brand risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abtdomain](https://clawhub.ai/user/abtdomain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, domain researchers, and brand teams use this skill to connect an agent to DomainKits for domain availability checks, WHOIS and DNS lookups, market pricing, trend research, and domain naming workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Domain searches, brand ideas, and analysis requests are sent to the DomainKits remote service. <br>
Mitigation: Use the skill only when sending that domain research data to DomainKits is acceptable for the project. <br>
Risk: The optional DOMAINKITS_API_KEY grants account features or higher limits. <br>
Mitigation: Provide an API key only when needed, store it securely, and avoid exposing it in shared prompts, logs, or configuration examples. <br>
Risk: Available-domain results can include registration links that may be affiliate or third-party links. <br>
Mitigation: Review registration links and pricing before acting on them, and disclose affiliate links in user-facing output. <br>
Risk: Optional preferences, monitors, or strategies can save account data for later use. <br>
Mitigation: Keep memory features disabled unless needed, and review, update, or delete saved preferences, monitors, and strategies when they are no longer required. <br>


## Reference(s): <br>
- [DomainKits MCP](https://domainkits.com/mcp) <br>
- [ClawHub Skill Page](https://clawhub.ai/abtdomain/domain) <br>
- [Abtdomain Publisher Profile](https://clawhub.ai/user/abtdomain) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and domain research results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include domain availability, prices, register URLs, WHOIS or DNS findings, safety checks, brand-risk notes, and account usage information.] <br>

## Skill Version(s): <br>
2.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
