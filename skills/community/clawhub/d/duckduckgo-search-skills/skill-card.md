## Description: <br>
Search the web using DuckDuckGo with no API key, supporting instant-answer and HTML search modes as a privacy-focused search alternative. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cscsxx606](https://clawhub.ai/user/cscsxx606) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run lightweight DuckDuckGo searches from a command line or agent workflow and receive result titles, URLs, snippets, and optional summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to DuckDuckGo and may expose sensitive queries. <br>
Mitigation: Avoid searching for secrets, credentials, private internal URLs, personal data, or other confidential information. <br>
Risk: Returned titles, snippets, URLs, and fetched page content are untrusted web content. <br>
Mitigation: Review results before using them in downstream agent actions, citations, commands, or generated decisions. <br>
Risk: DuckDuckGo HTML scraping can be rate limited or blocked, and parsed results may be incomplete. <br>
Mitigation: Use modest request rates, retry later after 403 errors, and prefer a supported search API for production workflows that require reliability. <br>


## Reference(s): <br>
- [DuckDuckGo](https://duckduckgo.com) <br>
- [DuckDuckGo Instant Answer API](https://api.duckduckgo.com/) <br>
- [DuckDuckGo HTML Search Endpoint](https://html.duckduckgo.com/html/) <br>
- [ClawHub Skill Page](https://clawhub.ai/cscsxx606/duckduckgo-search-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text search results or JSON with result objects and optional summary text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include titles, URLs, snippets, source labels, and optional summary fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
