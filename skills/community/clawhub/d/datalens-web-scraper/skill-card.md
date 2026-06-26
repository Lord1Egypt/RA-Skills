## Description: <br>
Uses DataLens MCP tools to scrape structured lists, tables, comments, products, reviews, and other repeating data from a website open in Chrome. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weird94](https://clawhub.ai/user/weird94) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to extract structured webpage data from an active Chrome session, preview small scraping runs, manage jobs, and export results for downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad access to a live Chrome session and exported webpage data. <br>
Mitigation: Use it only on pages intentionally selected for scraping, avoid sensitive logged-in accounts unless data exposure is understood, and review exports after use. <br>
Risk: The workflow depends on third-party DataLens npm and Chrome extension components. <br>
Mitigation: Install and use the DataLens package and extension only when the publisher and extension source are trusted. <br>
Risk: A scraping job can collect incorrect or unintended fields if started without validating the detected structure. <br>
Mitigation: Run column analysis first, inspect the returned fields, and perform a small preview run before full extraction. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/weird94/datalens-web-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with bash commands and JSON arguments; scraped data can be exported as JSON, CSV, or XLSX.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18 or newer, the DataLens npm package, the DataLens Chrome extension, and Chrome access to the target page.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
