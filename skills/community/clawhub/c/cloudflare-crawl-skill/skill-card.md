## Description:

Crawl websites using Cloudflare's Browser Rendering API to collect HTML, Markdown, or AI-extracted JSON from multiple pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wirelessjoe](https://clawhub.ai/user/wirelessjoe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content engineers use this skill to start, monitor, retrieve, and cancel Cloudflare Browser Rendering crawl jobs for site scraping, knowledge-base creation, research, and RAG dataset preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloudflare credentials are required to run crawl jobs.

Mitigation: Use a least-privilege Cloudflare API token limited to the Browser Rendering permission and rotate it according to your credential policy.

Risk: Target URLs, crawl settings, extraction prompts, and crawl results are processed by Cloudflare.

Mitigation: Avoid private, regulated, authenticated, or internal content unless you have approval and understand Cloudflare's retention and billing implications.

Risk: Large crawl jobs can consume Cloudflare Browser Rendering quota or incur usage costs.

Mitigation: Set conservative crawl limits and depth values before running jobs, then monitor job status and browser time.

## Reference(s):

- [Cloudflare Crawl Skill on ClawHub](https://clawhub.ai/wirelessjoe/skills/cloudflare-crawl-skill)
- [wirelessjoe ClawHub Profile](https://clawhub.ai/user/wirelessjoe)
- [Cloudflare API Tokens](https://dash.cloudflare.com/profile/api-tokens)
- [Cloudflare Browser Rendering Crawl API Endpoint](https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/browser-rendering/crawl)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JavaScript examples, and optional JSON crawl output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID; crawl results may include HTML, Markdown, or JSON.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
