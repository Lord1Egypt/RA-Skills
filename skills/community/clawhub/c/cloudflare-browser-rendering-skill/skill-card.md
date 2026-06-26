## Description: <br>
Use Cloudflare Browser Rendering REST APIs to extract rendered webpage content as Markdown or crawl whole sites asynchronously. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cytwyatt](https://clawhub.ai/user/cytwyatt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when lightweight fetching misses JavaScript-rendered content or when they need to crawl related documentation, help center, or knowledge-base pages for summarization, search, monitoring, or RAG preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cookies, login credentials, private HTML, or other sensitive page data may be sent to Cloudflare when users enable the supported auth, cookie, or HTML options. <br>
Mitigation: Use a least-privilege Cloudflare token and avoid passing real session cookies, passwords, or private HTML unless sending that data to Cloudflare is intended and covered by the user's logging and retention plan. <br>
Risk: Broad crawls can consume rendering capacity, run longer than expected, or generate large outputs that are hard to review. <br>
Mitigation: Start with low crawl depth and modest limits, poll lightly, fetch completed records selectively, and save large JSON or Markdown outputs to files before summarizing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cytwyatt/cloudflare-browser-rendering-skill) <br>
- [Project homepage](https://github.com/cytwyatt/cloudflare-browser-rendering-skill) <br>
- [Decision guide](references/decision-guide.md) <br>
- [Markdown endpoint notes](references/markdown-endpoint.md) <br>
- [Crawl endpoint notes](references/crawl-endpoint.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown or JSON returned by Python helpers, with optional saved JSON and Markdown files for crawl results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 plus CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID; crawl outputs can be large and should be filtered or summarized before sharing.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
