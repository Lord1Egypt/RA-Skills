## Description:

An end-to-end AI content pipeline that crawls articles, rewrites them using Google Gemini, and can publish the generated content to a Facebook Page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yunneetoichoi](https://clawhub.ai/user/yunneetoichoi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and social media operators use this skill to crawl news or public Facebook URLs, rewrite content with AI, optionally generate imagery, and publish, schedule, or dry-run posts for a Facebook Page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release ships live-looking credentials and token material.

Mitigation: Remove the bundled .env before installation, rotate every exposed credential, and replace it with a placeholder .env.example.

Risk: Publish mode can post AI-generated content to a Facebook Page without a required approval step.

Mitigation: Use dry-run by default and require explicit human approval before every Facebook publish or scheduled publish action.

Risk: Facebook Page tokens can grant broad posting permissions.

Mitigation: Limit token scopes to the minimum required Page permissions and rotate tokens when users or deployment environments change.

Risk: The crawler processes external URLs and may reach unintended destinations.

Mitigation: Run crawling in an isolated environment that cannot access private or internal network resources.

Risk: Dependencies are specified with lower bounds rather than exact pinned versions.

Mitigation: Pin dependencies and review updates before deployment.

## Reference(s):

- [ClawHub Release Page](https://clawhub.ai/yunneetoichoi/skills/asdsadasd)
- [Facebook Graph API Overview](artifact/skills/facebook/references/graph-api-overview.md)
- [Page Posting Guide](artifact/skills/facebook/references/page-posting.md)
- [Permissions and Tokens](artifact/skills/facebook/references/permissions-and-tokens.md)
- [HTTP Request Templates](artifact/skills/facebook/references/http-request-templates.md)
- [Comments and Moderation](artifact/skills/facebook/references/comments-moderation.md)
- [Webhooks](artifact/skills/facebook/references/webhooks.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [CLI output, generated Facebook post text, image prompts, and optional JSON report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save analysis results and run results under output/; publish mode may call Facebook Graph API unless dry-run is used.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and changelog mention 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
