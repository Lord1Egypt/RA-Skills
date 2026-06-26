## Description: <br>
Unified social data API for AI agents. One API key for LinkedIn, YouTube, TikTok, X, Instagram, Reddit, and Facebook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaencarrodine](https://clawhub.ai/user/jaencarrodine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover and call agntdata's unified social-data APIs across LinkedIn, YouTube, TikTok, X, Instagram, Reddit, and Facebook, including webhook setup and delivery polling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AGNTDATA_API_KEY and webhook receive URLs are sensitive credentials. <br>
Mitigation: Store them as secrets, avoid logging or sharing them, and rotate exposed values. <br>
Risk: Webhook endpoints use URL-only authentication and may persist raw third-party payloads. <br>
Mitigation: Avoid production webhooks unless sender authenticity can be independently verified and payloads are sanitized before processing. <br>
Risk: Social-data and contact-data queries may disclose sensitive data to agntdata. <br>
Mitigation: Minimize lookup scope and confirm the use case complies with applicable data-handling policies. <br>
Risk: The skill recommends a separate npm plugin for richer tooling. <br>
Mitigation: Review the plugin artifact and permissions separately before installing it. <br>


## Reference(s): <br>
- [agntdata homepage](https://agntdata.dev) <br>
- [agnt-data on ClawHub](https://clawhub.ai/jaencarrodine/agnt-data) <br>
- [Facebook API Reference](references/facebook/README.md) <br>
- [Instagram API Reference](references/instagram/README.md) <br>
- [LinkedIn API Reference](references/linkedin/README.md) <br>
- [Reddit API Reference](references/reddit/README.md) <br>
- [TikTok API Reference](references/tiktok/README.md) <br>
- [X API Reference](references/x/README.md) <br>
- [YouTube API Reference](references/youtube/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with curl commands, endpoint tables, and JSON response expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGNTDATA_API_KEY for authenticated API calls; public discovery endpoints are documented separately.] <br>

## Skill Version(s): <br>
1.0.15 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
