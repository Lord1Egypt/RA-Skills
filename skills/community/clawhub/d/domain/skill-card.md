## Description: <br>
Check domain availability, search domains across registration lifecycle stages, analyze domain registrations and keyword trends, and help agents act as domain research assistants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abtdomain](https://clawhub.ai/user/abtdomain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, domain researchers, marketers, and business users use this skill to check domain availability, compare TLD pricing, inspect WHOIS/DNS/safety signals, monitor domain changes, and generate or evaluate domain ideas through the DomainKits MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Domain names, keywords, business ideas, and analysis targets may be sent to the external DomainKits MCP service. <br>
Mitigation: Install only if that data sharing is acceptable, use secure secret handling for DOMAINKITS_API_KEY, and enable memory-backed preferences, monitors, or strategies only for information suitable for storage with the service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abtdomain/skills/domain) <br>
- [DomainKits MCP](https://domainkits.com/mcp) <br>
- [DomainKits API endpoint](https://api.domainkits.com/v1/mcp) <br>
- [DomainKits website](https://domainkits.com) <br>
- [ABTdomain](https://abtdomain.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with command and JSON configuration examples plus domain analysis results from MCP tools] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses DOMAINKITS_API_KEY for higher limits; account or memory features are required for some analysis, preferences, monitoring, and strategy tools.] <br>

## Skill Version(s): <br>
2.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
