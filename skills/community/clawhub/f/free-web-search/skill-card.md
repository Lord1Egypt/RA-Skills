## Description: <br>
Free Web Search is a Playwright-based web search skill that routes explicit search requests to Bing CN or DuckDuckGo, returns structured results, and can optionally fetch page text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ucsdzehualiu](https://clawhub.ai/user/ucsdzehualiu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill when they explicitly need live web search results, especially Chinese-language queries, with optional full-page text retrieval for selected results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search and routing send the user's IP address, user agent, and query text to external IP-location and search providers. <br>
Mitigation: Use the skill only in environments where those outbound requests are acceptable, and avoid submitting sensitive query text. <br>
Risk: Optional full-page fetching visits result pages and may disclose the user's IP address, user agent, and referer to those sites. <br>
Mitigation: Keep full-page fetching disabled unless page retrieval is needed; use the default full=0 posture for ordinary searches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ucsdzehualiu/free-web-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON search results with title, URL, snippet, and optional page text; documentation examples use Markdown with shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results are capped at 20 items; optional full-page fetching is capped at 5 results with page text truncated to 8000 characters.] <br>

## Skill Version(s): <br>
8.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
