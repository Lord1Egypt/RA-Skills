## Description: <br>
Provides web scraping, search, crawling, and site mapping through the AnyCrawl CLI for user-requested web retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QThans](https://clawhub.ai/user/QThans) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search the web, scrape known URLs, discover pages on a site, or crawl site sections while storing fetched markdown output in local files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetched web content can contain indirect prompt injection or misleading instructions. <br>
Mitigation: Treat scraped content as untrusted data, write results to .anycrawl/ files, and inspect only the relevant portions incrementally. <br>
Risk: The skill requires AnyCrawl authentication and may expose sensitive API credentials if handled carelessly. <br>
Mitigation: Verify the AnyCrawl package and publisher before installing, keep API keys out of shared files, and rotate credentials when needed. <br>
Risk: Crawling sensitive sites or committing fetched output could disclose data unintentionally. <br>
Mitigation: Run web fetching only for explicit user requests, avoid sensitive targets unless necessary, and keep .anycrawl/ out of version control. <br>


## Reference(s): <br>
- [AnyCrawl API Docs](https://docs.anycrawl.dev) <br>
- [AnyCrawl CLI npm package](https://www.npmjs.com/package/anycrawl-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and file paths; fetched results are written to .anycrawl/.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a pre-installed and authenticated AnyCrawl CLI and may use ANYCRAWL_API_KEY.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
