## Description: <br>
Web search without an API key using DuckDuckGo Lite via web_fetch, providing titles, URLs, and snippets for research queries when no search API is configured. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JakeLin](https://clawhub.ai/user/JakeLin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run lightweight web searches through DuckDuckGo Lite, then select and fetch relevant result pages for research. It is useful when a configured search API is unavailable or no API key is present. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes external network requests to DuckDuckGo Lite and fetched result pages. <br>
Mitigation: Use it only where outbound web access is permitted and review selected result URLs before fetching page content. <br>
Risk: Search results can include sponsored links or outdated, incomplete, or irrelevant snippets. <br>
Mitigation: Skip sponsored entries, fetch primary sources where possible, and corroborate important claims before relying on them. <br>


## Reference(s): <br>
- [DuckDuckGo Search Parameters](https://duckduckgo.com/params) <br>
- [ClawHub skill listing](https://clawhub.ai/JakeLin/ddg-web-search) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text] <br>
**Output Format:** [Markdown instructions with web_fetch URL examples and text search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output depends on DuckDuckGo Lite availability and may include sponsored results that should be skipped.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
