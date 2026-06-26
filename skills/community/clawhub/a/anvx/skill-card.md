## Description: <br>
Track and optimize AI API spending across 19 providers with live pricing and 6 optimization modules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tje8x](https://clawhub.ai/user/tje8x) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and finance teams use this skill to analyze AI, cloud, payments, communications, monitoring, data-tool, and crypto-related spending, then generate cost optimization recommendations from connected read-only accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests access to sensitive financial, operational, exchange, and possible bank-CSV data. <br>
Mitigation: Use only restricted read-only credentials, connect only the providers needed, avoid wallet seed phrases or write-enabled exchange keys, and review organizational approval before processing financial records. <br>
Risk: Financial record details may be sent to Anthropic for categorization and natural-language analysis. <br>
Mitigation: Use data approved for Anthropic processing, redact records that should not leave the local environment, and confirm the required ANTHROPIC_API_KEY is managed under the intended account. <br>
Risk: The skill persists cache, model, and event data under ~/.token-economy-intel. <br>
Mitigation: Review local file permissions and retention expectations, and clear the local cache or event log when the data is no longer needed. <br>
Risk: Telemetry is disabled by default but can send events when ANALYTICS_ENABLED=true and ANALYTICS_ENDPOINT is configured. <br>
Mitigation: Leave analytics disabled unless the endpoint is approved, and verify event payloads exclude financial amounts, credentials, wallet addresses, and personal data before enabling. <br>


## Reference(s): <br>
- [ANVX homepage](https://anvx.io) <br>
- [ClawHub skill page](https://clawhub.ai/tje8x/anvx) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and natural-language text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Financial summaries, anomaly alerts, provider status, and optimization recommendations may include dollar amounts, percentages, and service names.] <br>

## Skill Version(s): <br>
1.4.6 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
