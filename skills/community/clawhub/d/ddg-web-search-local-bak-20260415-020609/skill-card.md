## Description: <br>
Search the web with DuckDuckGo instant answer API and return concise results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[graafdefolkert-byte](https://clawhub.ai/user/graafdefolkert-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to perform quick web lookups, fetch concise facts, and return source URLs without browser automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to DuckDuckGo. <br>
Mitigation: Use only queries that are appropriate to share with DuckDuckGo and avoid including secrets or sensitive private data. <br>
Risk: The optional --open flag can launch a local browser to a returned URL. <br>
Mitigation: Use --open only when intentionally opening a result, and review returned URLs before visiting them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/graafdefolkert-byte/ddg-web-search-local-bak-20260415-020609) <br>
- [DuckDuckGo Instant Answer API endpoint](https://api.duckduckgo.com/) <br>
- [DuckDuckGo HTML search endpoint](https://duckduckgo.com/html/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text with concise summaries and source URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May print related topics, fallback web results, or a clear no-result message.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
