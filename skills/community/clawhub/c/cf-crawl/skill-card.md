## Description: <br>
Crawl websites using the Cloudflare Browser Rendering /crawl API with async multi-page crawling, markdown/HTML/JSON output, link following, pattern filtering, and AI-powered structured data extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bill492](https://clawhub.ai/user/bill492) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to crawl multi-page websites through Cloudflare Browser Rendering when basic fetch tools are insufficient, including JavaScript-rendered pages, filtered crawls, knowledge-base ingestion, and structured data extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloudflare credentials are required to run crawl and poll commands. <br>
Mitigation: Store the token carefully and prefer a least-privileged Cloudflare token with only the access needed for Browser Rendering. <br>
Risk: Large, deep, rendered, external-link, or JSON extraction crawls can create network, cost, and data-volume exposure. <br>
Mitigation: Start with small limits and shallow depth, avoid external-link crawling unless required, and review paid browser rendering and JSON extraction options before running large jobs. <br>
Risk: Crawl results may be written to output files and can contain website content returned by Cloudflare. <br>
Mitigation: Choose output paths deliberately and review generated files before sharing or ingesting them downstream. <br>


## Reference(s): <br>
- [Cloudflare /crawl API Reference](references/api-reference.md) <br>
- [ClawHub cf-crawl Release Page](https://clawhub.ai/bill492/cf-crawl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Markdown, HTML, JSON, and shell command output from Cloudflare crawl jobs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write full crawl results to a user-specified output file; raw API responses are available with --raw.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
