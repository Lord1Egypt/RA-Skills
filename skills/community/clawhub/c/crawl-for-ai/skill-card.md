## Description: <br>
Full web page scraping with JavaScript rendering via a local Crawl4AI instance, delivering clean markdown or detailed JSON including links and media. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[angusthefuzz](https://clawhub.ai/user/angusthefuzz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to fetch web page content from a trusted Crawl4AI instance when JavaScript rendering or detailed page metadata is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured Crawl4AI service receives the URLs requested for crawling and may receive a bearer token when CRAWL4AI_KEY is set. <br>
Mitigation: Use only a Crawl4AI endpoint you control or trust, set CRAWL4AI_URL deliberately, and set CRAWL4AI_KEY only for trusted endpoints. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/angusthefuzz/crawl-for-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON] <br>
**Output Format:** [Markdown text by default, or formatted JSON when --json is used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CRAWL4AI_URL; sends requested URLs to the configured Crawl4AI service.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
