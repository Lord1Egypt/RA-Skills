## Description: <br>
Crawl websites using Cloudflare's Browser Rendering API to scrape entire sites, build knowledge bases, extract multipage content, and return HTML, Markdown, or AI-extracted JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wirelessjoe](https://clawhub.ai/user/wirelessjoe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to start, monitor, cancel, and retrieve Cloudflare Browser Rendering crawl jobs for site scraping, research, knowledge-base creation, and RAG dataset preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloudflare credentials are required to run crawl jobs. <br>
Mitigation: Use a least-privilege Cloudflare API token with only the required Browser Rendering permission and keep CLOUDFLARE_API_TOKEN out of shared logs and files. <br>
Risk: Crawled pages may include private or sensitive content. <br>
Mitigation: Crawl only sites you are authorized to process and store outputs in locations with appropriate access controls. <br>
Risk: Verbose and JSON modes can print crawled content to terminal logs. <br>
Mitigation: Avoid --verbose and --json for sensitive targets, or redirect output only to protected storage. <br>
Risk: Large crawl limits or depths can increase cost and operational impact. <br>
Mitigation: Set modest --limit and --depth values and cancel jobs that are no longer needed. <br>


## Reference(s): <br>
- [Cloudflare Crawl on ClawHub](https://clawhub.ai/wirelessjoe/cloudflare-crawl-skill) <br>
- [Cloudflare API Tokens](https://dash.cloudflare.com/profile/api-tokens) <br>
- [Cloudflare Browser Rendering Crawl API](https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/browser-rendering/crawl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, plus CLI text or JSON crawl results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID. The CLI can return job status, paginated result summaries, verbose content previews, or raw JSON.] <br>

## Skill Version(s): <br>
0.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
