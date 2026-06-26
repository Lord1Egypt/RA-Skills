## Description: <br>
Web scraping and crawling with the Firecrawl API, including markdown capture, screenshots, structured extraction, web search, documentation crawling, and URL mapping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[capt-marbles](https://clawhub.ai/user/capt-marbles) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to retrieve current web content, capture screenshots, extract structured data from pages, search the web, and crawl or map documentation sites through Firecrawl. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested URLs, search terms, extraction prompts, and schemas are sent to Firecrawl. <br>
Mitigation: Avoid private or sensitive URLs unless Firecrawl is approved for that data, and use a Firecrawl key with suitable account limits. <br>
Risk: Crawls, maps, screenshots, and searches can consume Firecrawl credits or account quota. <br>
Mitigation: Keep crawl and map limits modest and review requested operations before execution. <br>
Risk: Dependency behavior can change if the Firecrawl SDK version floats. <br>
Mitigation: Consider pinning the Firecrawl SDK version for repeatable deployments. <br>


## Reference(s): <br>
- [Firecrawl](https://firecrawl.dev) <br>
- [Firecrawl API Keys](https://www.firecrawl.dev/app/api-keys) <br>
- [ClawHub Skill Page](https://clawhub.ai/capt-marbles/firecrawler) <br>
- [Publisher Profile](https://clawhub.ai/user/capt-marbles) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, plaintext URL lists, shell command examples, and PNG screenshot files depending on the command.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FIRECRAWL_API_KEY and may save crawl output or screenshots to local files when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
