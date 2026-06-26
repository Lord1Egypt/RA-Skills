## Description: <br>
Quota-aware multi-provider web search for OpenClaw with automatic failover, task-level deep search (@dual/@deep), real quota checks, and managed result storage under memory/. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[VulcanusALex](https://clawhub.ai/user/VulcanusALex) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to run quota-aware web searches across multiple providers, aggregate task-level research results, check provider quota and health, and persist search outputs under memory/. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms may be sent to configured third-party search providers. <br>
Mitigation: Avoid entering secrets or regulated data as queries, and configure only providers approved for the deployment context. <br>
Risk: Search results and related metadata are stored locally under memory/. <br>
Mitigation: Review local retention, logs, and access controls before use in sensitive environments. <br>
Risk: Self-hosted provider endpoints can affect data exposure and result integrity. <br>
Mitigation: Use trusted self-hosted endpoints only and pin dependencies for production or sensitive environments. <br>


## Reference(s): <br>
- [Free Search Aggregator on ClawHub](https://clawhub.ai/VulcanusALex/free-search-aggregator) <br>
- [Mojeek Search API](https://www.mojeek.com/services/search/api/) <br>
- [Exa](https://exa.ai/) <br>
- [Google Custom Search JSON API](https://developers.google.com/custom-search/v1/introduction) <br>
- [Google Programmable Search Engine](https://programmablesearchengine.google.com/) <br>
- [Baidu Cloud](https://cloud.baidu.com/) <br>
- [SearXNG](https://searxng.github.io/searxng/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON search payloads, Markdown reports, and shell/Python command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists search cache, index, reports, provider health, and discovery records under memory/.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
