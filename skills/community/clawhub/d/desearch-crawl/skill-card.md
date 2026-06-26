## Description: <br>
Crawl/scrape and extract content from any webpage URL. Returns the page content as clean text or raw HTML. Use this when you need to read the full contents of a specific web page. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okradze](https://clawhub.ai/user/okradze) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to fetch a webpage through Desearch and receive the page content as clean text or raw HTML for reading, summarization, analysis, or inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested URLs and returned page data are processed by the external Desearch service. <br>
Mitigation: Use the skill only for URLs that are acceptable to send to Desearch, and avoid intranet, localhost, authenticated, confidential, or token-bearing URLs unless that external processing is approved. <br>
Risk: The skill requires a Desearch API key. <br>
Mitigation: Use a dedicated DESEARCH_API_KEY that can be rotated or revoked, and provide it through the environment rather than embedding it in prompts or files. <br>


## Reference(s): <br>
- [Crawl By Desearch on ClawHub](https://clawhub.ai/okradze/desearch-crawl) <br>
- [Desearch Homepage](https://desearch.ai) <br>
- [Desearch Web Crawl API Reference](https://desearch.ai/docs/api-reference/get-web-crawl) <br>
- [Desearch Console](https://console.desearch.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, html, shell commands, guidance] <br>
**Output Format:** [Plain text or raw HTML from crawled webpages; JSON may be printed for service errors.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DESEARCH_API_KEY and sends requested URLs to the external Desearch service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
