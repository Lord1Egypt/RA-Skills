## Description: <br>
Scrape, search, map, and crawl the web for AI agents via the Firecrawl API when an agent needs clean markdown from JavaScript-heavy sites, search results with full page content, site URL mapping, or deep documentation crawls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dyagil](https://clawhub.ai/user/dyagil) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to decide when to use Firecrawl instead of basic fetching, then run Firecrawl scrape, search, map, crawl, status, and REST API commands for web-data collection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Firecrawl API key and can interact with authenticated or sensitive web pages. <br>
Mitigation: Store the API key only in the documented credentials file, avoid sending personal data unless necessary, and require explicit approval before scraping authenticated content or form fields. <br>
Risk: Large map and crawl commands can consume paid Firecrawl credits. <br>
Mitigation: Set a crawl or map limit before execution and ask the user to confirm expected credit use for large jobs. <br>
Risk: Login-page automation and anti-bot bypass prompts can cross access-control or site-policy boundaries. <br>
Mitigation: Require user approval before login-page interaction, form filling, or attempting to bypass anti-bot or access controls. <br>
Risk: Scraped or searched content can be incomplete, stale, or misleading. <br>
Mitigation: Review important extracted content against source pages before relying on it for decisions or publication. <br>


## Reference(s): <br>
- [Firecrawl website](https://firecrawl.dev) <br>
- [Firecrawl documentation](https://docs.firecrawl.dev) <br>
- [ClawHub skill page](https://clawhub.ai/dyagil/dyagil-firecrawl) <br>
- [dyagil publisher profile](https://clawhub.ai/user/dyagil) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON REST examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Firecrawl CLI commands, API request examples, credential setup guidance, and cost-aware crawl limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
