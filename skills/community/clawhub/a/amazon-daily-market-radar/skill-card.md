## Description: <br>
Automates daily Amazon market monitoring for sellers by tracking ASINs, competitors, price changes, BSR movement, review spikes, stock-out signals, and market shifts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apiclaw](https://clawhub.ai/user/apiclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Amazon sellers and marketplace operators use this skill to set up APIClaw-backed daily monitoring for their products, competitors, and market shifts. It produces alert-prioritized briefings and action guidance from sampled Amazon market data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIClaw processes submitted Amazon ASINs, keywords, categories, and competitor-monitoring queries. <br>
Mitigation: Use a dedicated APIClaw key, avoid sending sensitive or unnecessary product data, and invoke the skill only for explicit Amazon or APIClaw monitoring tasks. <br>
Risk: Scheduled or repeated monitoring can make external API calls and consume API credits. <br>
Mitigation: Schedule runs only when recurring monitoring is intended, monitor credit usage, and keep alert preferences scoped to the products and competitors that need tracking. <br>
Risk: Market conclusions rely on sampled API data and lower-bound sales estimates. <br>
Mitigation: Treat generated recommendations as decision support, keep the required disclaimer, and validate important business actions with additional sources before acting. <br>


## Reference(s): <br>
- [APIClaw Field Reference](references/reference.md) <br>
- [APIClaw API Documentation](https://api.apiclaw.io/api-docs) <br>
- [APIClaw API Key Setup](https://apiclaw.io/en/api-keys) <br>
- [ClawHub Skill Page](https://clawhub.ai/apiclaw/amazon-daily-market-radar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown briefing with alert sections, KPI tables, data provenance, API usage, and action items.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses APICLAW_API_KEY and APIClaw API sampling; first run establishes a baseline and later runs compare against the previous snapshot.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
