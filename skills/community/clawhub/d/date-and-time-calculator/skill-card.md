## Description: <br>
Date And Time Calculator helps agents perform date arithmetic, business-day counts, timezone conversion, duration parsing and formatting, Unix timestamp conversion, ISO week lookup, quarter lookup, leap-year checks, and working-hours overlap checks through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when they need AgentPMT's hosted date and time tools for scheduling, project duration calculations, timestamp conversion, countdowns, fiscal-quarter lookup, and timezone-aware workflow checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote AgentPMT calls may require account credentials and may consume credits. <br>
Mitigation: Install this skill only when using AgentPMT-hosted date/time tools, and review the AgentPMT setup skills before connecting account, REST, or MCP credentials. <br>
Risk: Credentials, wallet material, signatures, or payment headers could be exposed if placed in prompts or logs. <br>
Mitigation: Keep secrets, wallet private keys, mnemonics, signatures, and payment headers out of prompts and logs. <br>
Risk: Business-day calculations count weekdays only and do not account for public holidays. <br>
Mitigation: Apply holiday calendars or business-specific exceptions outside the tool when holiday-aware scheduling is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/date-and-time-calculator) <br>
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/date-calculator-and-timestamp-tool-set) <br>
- [AgentPMT setup skill](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>
- [schema.md](artifact/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, code] <br>
**Output Format:** [Markdown instructions with JSON request bodies, shell command examples, and schema references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote calls return JSON from AgentPMT-hosted tools; live schema lookups are recommended before production integrations when parameters or response shapes are unclear.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
