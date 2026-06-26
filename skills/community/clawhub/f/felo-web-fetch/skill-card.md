## Description: <br>
Fetches webpage content from a URL through the Felo Web Extract API and returns HTML, text, or Markdown for agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to fetch page content, extract article text, or convert a URL into Markdown or plain text for summarization, analysis, or downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested URLs, query parameters, selectors, and fetched results are handled by Felo's external service. <br>
Mitigation: Avoid using the skill for private intranet links, authenticated documents, secret-bearing URLs, or regulated data unless third-party sharing through Felo is approved. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wangzhiming1999/felo-web-fetch) <br>
- [Felo Web Extract API](https://openapi.felo.ai/docs/api-reference/v2/web-extract.html) <br>
- [Felo Open Platform](https://openapi.felo.ai/docs/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, plain text, HTML, or JSON API response depending on selected options] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FELO_API_KEY and sends requested URLs, selectors, and fetch parameters to Felo's external API.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
