## Description: <br>
Helps agents choose and run Firecrawl CLI commands to scrape pages, crawl sites, discover URLs, search and scrape results, run autonomous data gathering, and extract structured data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariokarras](https://clawhub.ai/user/mariokarras) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to collect web content and structured data through Firecrawl CLI workflows for single-page scraping, site crawling, URL discovery, search-backed extraction, and LLM-based structured extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URLs, prompts, and retrieved content may be sent to Firecrawl as a third-party service. <br>
Mitigation: Avoid confidential, internal, authenticated, personal-data-heavy, or terms-restricted sites unless the user has permission, and avoid including secrets or proprietary research details in prompts or crawl requests. <br>
Risk: Firecrawl API access requires a FIRECRAWL_API_KEY, which could be exposed if pasted into prompts or command text. <br>
Mitigation: Keep the API key in the environment, do not print or embed it in generated commands, and use --dry-run when previewing requests. <br>


## Reference(s): <br>
- [Firecrawl](https://firecrawl.dev) <br>
- [ClawHub release page](https://clawhub.ai/mariokarras/abm-firecrawl-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should identify source URLs, extraction method, and extracted content; live Firecrawl commands require FIRECRAWL_API_KEY, while --dry-run can preview requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
