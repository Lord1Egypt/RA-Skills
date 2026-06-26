## Description: <br>
Simple web search using multiple search engines with no API key required. Supports Google, Bing, DuckDuckGo, Baidu, Sogou, 360, Brave, Yandex. Features time filtering, interactive mode, snippet extraction, and network diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hkall](https://clawhub.ai/user/hkall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run web searches across multiple public search engines, retrieve snippets, apply time filters, and format results for downstream reading or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to public search engines and may also pass through a configured proxy. <br>
Mitigation: Avoid searching for secrets, credentials, private customer data, or internal-only project details. <br>
Risk: Automatic fallback can route a query to a different search engine than expected. <br>
Mitigation: Use a specific engine and --no-fallback when query routing needs tighter control. <br>
Risk: Search results are cached locally for faster repeated searches. <br>
Mitigation: Use --clear-cache after sensitive workflows and avoid submitting sensitive queries. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/hkall/easy-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, CSV, shell commands, guidance] <br>
**Output Format:** [Search results and diagnostics as JSON, Markdown, simple text, or CSV] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports result count, engine selection, time filtering, interactive mode, proxy-aware requests, and local cache clearing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
