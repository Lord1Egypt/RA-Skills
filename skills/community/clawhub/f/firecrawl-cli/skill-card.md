## Description: <br>
Web scraping, crawling, search, browser automation, and natural-language web queries through the Firecrawl CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Yash-Kavaiya](https://clawhub.ai/user/Yash-Kavaiya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to choose Firecrawl CLI commands for scraping individual pages, crawling sites, discovering URLs, running web searches, launching browser sessions, and asking Firecrawl's agent to perform web research tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Third-party web scraping and browser automation can expose sensitive URLs, page content, private prompts, or logged-in browser state. <br>
Mitigation: Avoid sensitive internal URLs, confidential content, private prompts, and logged-in browser profiles unless approved; use a self-hosted Firecrawl endpoint for sensitive environments. <br>
Risk: Broad crawl, search, browser, or agent jobs can consume credits or collect more content than intended. <br>
Mitigation: Use crawl limits, depth limits, concurrency controls, and maximum credit settings, and check Firecrawl status or credit usage before parallel or long-running jobs. <br>


## Reference(s): <br>
- [Firecrawl CLI Command Reference](references/commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may produce markdown, HTML, JSON, links, screenshots, or saved files depending on Firecrawl CLI options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
