## Description: <br>
FlowCrawl is a local OpenClaw web scraping skill that extracts website content as markdown, text, or JSON using a three-tier fetcher cascade that escalates from plain HTTP to stealth and JavaScript-based fetching when blocked. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[windseeker1111](https://clawhub.ai/user/windseeker1111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use FlowCrawl to extract clean content from authorized websites for research, knowledge-base ingestion, and data pipeline workflows. It can scrape a single URL or crawl same-site pages with depth and page limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is framed and implemented to bypass bot protections on arbitrary sites without built-in authorization controls. <br>
Mitigation: Install and run it only for authorized scraping or defensive testing of sites where the user has permission, and require users to respect site terms, robots.txt, and rate limits. <br>
Risk: Deep crawls can create unwanted load or collect more content than intended. <br>
Mitigation: Use conservative depth and page limits, review output paths before running, and keep the built-in crawl delay or stronger local throttling for sensitive targets. <br>
Risk: Recommended alias setup modifies the user's shell startup file. <br>
Mitigation: Review the alias command before applying it and add it manually when shell configuration changes need approval. <br>


## Reference(s): <br>
- [FlowCrawl ClawHub listing](https://clawhub.ai/windseeker1111/flowcrawl) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Scrapling](https://github.com/D4Vinci/Scrapling) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, JSON, Files, Shell commands] <br>
**Output Format:** [Markdown, plain text, structured JSON metadata, or saved .md/.txt files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports single-page scraping, same-site crawling with depth and page limits, optional combined output, quiet mode, and configurable output directories.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
