## Description: <br>
Web search via self-hosted SearxNG. Aggregates Google, Bing, DuckDuckGo, Brave. Returns title/url/snippet. Zero API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sexychina](https://clawhub.ai/user/sexychina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Ask Search to query a local SearxNG instance for web, news, language-filtered, or engine-filtered search results without an API key. It supports CLI and MCP workflows that return concise search snippets, URLs, or raw JSON for follow-up retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence flags under-scoped guidance around proxy-based scraping and logged-in browsing. <br>
Mitigation: Keep usage to normal SearxNG search where possible, and only use proxy, browser, or logged-in fetching workflows with authorization, supervision, and an isolated environment. <br>
Risk: Search results and snippets may be incomplete, outdated, or misleading when used without reviewing the source page. <br>
Mitigation: Treat results as candidates, inspect snippets, and fetch or verify original sources before relying on the information. <br>


## Reference(s): <br>
- [Ask Search ClawHub release](https://clawhub.ai/sexychina/ask-search) <br>
- [SearxNG](https://github.com/searxng/searxng) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Perplexica](https://github.com/ItzCrazyKns/Perplexica) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Plain text, URL lists, or JSON search-result objects with title, url, content, and engine fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI output is limited by the requested result count; the MCP tool caps standard web_search requests at 20 results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and scripts/core.py VERSION) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
