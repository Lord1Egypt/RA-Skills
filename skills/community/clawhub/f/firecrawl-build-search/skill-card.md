## Description: <br>
Integrate Firecrawl `/search` into product code and agent workflows for query-first source discovery, ranking, and optional content hydration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eohmig](https://clawhub.ai/user/eohmig) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill when an application starts from a search query and needs to discover, rank, and select web sources before optional scraping or extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries may expose secrets, regulated personal data, customer records, or confidential internal project details to Firecrawl or self-hosted search logs. <br>
Mitigation: Use this skill only with a Firecrawl deployment approved for the data being searched, and avoid sending sensitive query text unless logging and retention are acceptable. <br>


## Reference(s): <br>
- [Firecrawl homepage](https://www.firecrawl.dev) <br>
- [Firecrawl Node / TypeScript source-of-truth docs](https://docs.firecrawl.dev/agent-source-of-truth/node) <br>
- [Firecrawl Python source-of-truth docs](https://docs.firecrawl.dev/agent-source-of-truth/python) <br>
- [Firecrawl cURL / REST source-of-truth docs](https://docs.firecrawl.dev/agent-source-of-truth/curl) <br>
- [ClawHub release page](https://clawhub.ai/eohmig/firecrawl-build-search) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with optional code snippets, shell commands, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Firecrawl API key for hosted requests and may use a custom Firecrawl API URL for approved self-hosted deployments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
