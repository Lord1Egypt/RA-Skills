## Description: <br>
Professional DeFi data aggregator that provides unified access to TVL, protocols, chains, and yields data from DefiLlama. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deanpeng-dotcom](https://clawhub.ai/user/deanpeng-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External DeFi analysts, investors, and developers use this skill to query DefiLlama TVL, protocol, chain, and yield data from an agent workflow or CLI. It is useful for market monitoring, data export, and API health checks, but should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional IP-direct HTTPS mode disables certificate checks. <br>
Mitigation: Use the default domain-based DefiLlama configuration and do not enable IP-direct HTTPS mode. <br>
Risk: Market, TVL, and yield data can be stale, unavailable, or inaccurate because it depends on upstream DefiLlama and network responses. <br>
Mitigation: Cross-check important financial decisions with primary sources and do not rely on this skill alone for investment decisions. <br>
Risk: Installing the skill runs npm dependency installation. <br>
Mitigation: Review package dependencies and install only in environments where npm packages and public API requests are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deanpeng-dotcom/defillama-data-aggregator) <br>
- [Repository listed in metadata](https://github.com/AntalphaAI/defillama-data-aggregator) <br>
- [DefiLlama API](https://api.llama.fi) <br>
- [DefiLlama Yields API](https://yields.llama.fi) <br>
- [DefiLlama documentation](https://docs.llama.fi/) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, csv, shell commands, configuration, guidance] <br>
**Output Format:** [CLI output in pretty text, table, JSON, or CSV formats] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only public DefiLlama API requests with in-memory caching; no API key is required for the documented default configuration.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence, frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
