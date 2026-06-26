## Description: <br>
Creem Agent is an autonomous SaaS operations manager for Creem.io stores that monitors heartbeats, handles failed payments and churn, prepares revenue digests, and answers natural language queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vayospot](https://clawhub.ai/user/vayospot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and SaaS founders using Creem as their Merchant of Record use this skill to monitor store health, summarize revenue and subscriber metrics, respond to failed payments, and prepare churn recovery actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent recurring live Creem billing access and automatic account-changing authority. <br>
Mitigation: Use a narrowly scoped Creem API key if available, review Discord and webhook destinations, and require human approval outside the skill before creating discounts, sending customer-facing recovery links, or changing pricing-related store state. <br>
Risk: The security verdict is suspicious because recurring billing automation lacks enough user control. <br>
Mitigation: Install only when the operator is comfortable granting live billing access and has reviewed the configured automation paths. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vayospot/creem-agent) <br>
- [Creem Skill Instructions](https://creem.io/SKILL.md) <br>
- [Creem Heartbeat Instructions](https://creem.io/HEARTBEAT.md) <br>
- [Creem LLM Documentation](https://docs.creem.io/llms-full.txt) <br>
- [Creem Discounts API Endpoint](https://api.creem.io/v1/discounts) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands, JSON heartbeat output, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the creem, curl, and python3 binaries plus CREEM_API_KEY; heartbeat automation may emit HEARTBEAT_OK or JSON alerts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
