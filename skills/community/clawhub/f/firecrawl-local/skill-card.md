## Description: <br>
Firecrawl Local lets agents scrape pages, map sites, and crawl documentation through a trusted self-hosted Firecrawl v1 REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saddamtechie](https://clawhub.ai/user/saddamtechie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract clean web content, discover site URLs, and collect documentation content for ingestion or RAG workflows using a local Firecrawl service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scraping or crawling can collect private, sensitive, or unauthorized content if the skill is pointed at internal or restricted URLs. <br>
Mitigation: Use only authorized targets, avoid private or sensitive URLs unless permission is clear, and keep crawl scope conservative. <br>
Risk: FIRECRAWL_LOCAL_URL and FIRECRAWL_API_KEY determine where requests and any bearer token are sent. <br>
Mitigation: Set these values only for trusted self-hosted Firecrawl instances and protect any API key in the shell environment. <br>
Risk: Large crawls can consume service or site resources. <br>
Mitigation: Use --limit, --max-depth, --include, and --exclude to keep crawls scoped to the intended pages. <br>


## Reference(s): <br>
- [Firecrawl Local ClawHub release](https://clawhub.ai/saddamtechie/firecrawl-local) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Shell command invocations and JSON responses containing scraped markdown, HTML, links, metadata, or crawl result arrays.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and a reachable trusted Firecrawl service at FIRECRAWL_LOCAL_URL; crawl polling can run for up to five minutes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
