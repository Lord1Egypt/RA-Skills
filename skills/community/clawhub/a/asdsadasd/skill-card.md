## Description: <br>
An end-to-end AI Content Pipeline that crawls articles, rewrites them using Google Gemini, and automatically publishes to Facebook Fanpage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YunneeToiChoi](https://clawhub.ai/user/YunneeToiChoi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to crawl article or public Facebook URLs, generate localized social media copy, optionally create image assets, and publish or schedule posts to a Facebook Page. It supports single-URL, batch analysis, dry-run, and publish workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release ships live-looking API keys and Facebook tokens. <br>
Mitigation: Remove bundled credentials before installation, rotate any exposed keys or tokens, and provide secrets through a local environment manager. <br>
Risk: The publish and test-post commands can post directly to a Facebook Page. <br>
Mitigation: Keep dry-run mode as the default during testing, verify the Page ID is owned by the operator, and run publish commands only after human review. <br>
Risk: Facebook Page permissions can grant broad posting or engagement access. <br>
Mitigation: Use least-privilege Facebook permissions and review token scopes before connecting the skill to production Pages. <br>


## Reference(s): <br>
- [Facebook Graph API Overview](skills/facebook/references/graph-api-overview.md) <br>
- [Page Posting Guide](skills/facebook/references/page-posting.md) <br>
- [Permissions and Tokens](skills/facebook/references/permissions-and-tokens.md) <br>
- [HTTP Request Templates](skills/facebook/references/http-request-templates.md) <br>
- [Comments and Moderation](skills/facebook/references/comments-moderation.md) <br>
- [Webhooks](skills/facebook/references/webhooks.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, API Calls] <br>
**Output Format:** [CLI output, saved JSON reports, generated image files, and Facebook Graph API post responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can publish immediately, schedule posts, or run in dry-run mode depending on command options and configured credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
