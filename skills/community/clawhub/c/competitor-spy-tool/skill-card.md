## Description: <br>
Monitors competitor websites for pricing changes, new content, and keyword movements for competitive intelligence, market tracking, and SEO monitoring across multiple domains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ncreighton](https://clawhub.ai/user/ncreighton) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
SaaS founders, ecommerce managers, digital agencies, content strategists, and growth teams use this skill to monitor public competitor pricing pages, content updates, landing pages, and keyword movements, then summarize changes for review and response planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flagged advice to work around site blocking with rotating User-Agent headers or residential proxies. <br>
Mitigation: Do not use those techniques to continue scraping a site that has blocked automated access; keep monitoring to public pages you are allowed to access. <br>
Risk: The skill uses API keys and webhook destinations for SerpAPI, Slack, and Google Sheets. <br>
Mitigation: Use scoped credentials, dedicated Slack channels and Sheets, and rotate or revoke credentials if monitoring configuration is shared. <br>
Risk: Competitive monitoring can exceed an allowed scope if domains, frequency, retention, or deletion practices are not defined. <br>
Mitigation: Set explicit domain allowlists, request frequency limits, retention periods, and deletion procedures before deployment. <br>


## Reference(s): <br>
- [Competitor Spy Tool on ClawHub](https://clawhub.ai/ncreighton/competitor-spy-tool) <br>
- [SerpAPI](https://serpapi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and alert/report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces monitoring plans, configuration snippets, Slack alert examples, Google Sheets logging guidance, and competitive intelligence summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
