## Description: <br>
【极简版省token】使用 Brave API 执行网络搜索。针对国内代理环境做优化。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jhc888007](https://clawhub.ai/user/jhc888007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to run Brave web searches through a configured local proxy/VPN and return compact JSON search results for agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Brave through the configured local proxy/VPN. <br>
Mitigation: Avoid submitting secrets, private internal URLs, sensitive identifiers, or confidential business data as search terms. <br>
Risk: The skill requires a Brave API key and local proxy port through environment variables. <br>
Mitigation: Provide credentials through the agent's secret or environment configuration and do not commit real keys to repository files. <br>
Risk: The README suggests routing future searches to this skill and disabling another web search tool. <br>
Mitigation: Apply that routing only when Brave via the configured proxy should be the agent's intended search path. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jhc888007/brave-search-vpn) <br>
- [Publisher profile](https://clawhub.ai/user/jhc888007) <br>
- [Brave Search API](https://api.search.brave.com) <br>
- [Brave Search API keys](https://api-dashboard.search.brave.com/app/keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON string from the Brave Search CLI, with Markdown documentation and shell command examples for setup.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns compact web, news, and video result objects when available; requires BRAVE_SEARCH_API_KEY and HTTP_PROXY_PORT.] <br>

## Skill Version(s): <br>
1.0.6 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
