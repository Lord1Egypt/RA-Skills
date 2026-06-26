## Description: <br>
Web search and content fetching via Playwright and HTTP with no API keys; searches Bing CN or DuckDuckGo and can auto-fetch top page contents for real-time lookup, fact-checking, news, tutorials, and documentation lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ucsdzehualiu](https://clawhub.ai/user/ucsdzehualiu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to search the web and fetch page text from public URLs without configuring a paid search API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, region/IP metadata, and fetched URLs may be visible to search engines, IP-check services, and destination sites. <br>
Mitigation: Do not enter secrets, private internal URLs, or confidential research terms; use region overrides and disable automatic fetching when less browsing is appropriate. <br>
Risk: Fetching pages may load third-party content in Chromium when HTTP extraction is insufficient. <br>
Mitigation: Use the http-only fetch option for pages where browser rendering is not needed, and review fetched content before relying on it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ucsdzehualiu/free-web-search-js) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [JSON arrays containing search results, URLs, snippets, and fetched page content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output can include auto-fetched page text; fetch output is capped by the max-len option.] <br>

## Skill Version(s): <br>
29.1.0 (source: frontmatter, package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
