## Description:

Publishes prepared articles to WeChat Official Accounts by uploading article assets, creating drafts, running pre-publish checks, and optionally submitting public releases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiworkskills](https://clawhub.ai/user/aiworkskills)

### License/Terms of Use:

MIT-0

## Use Case:

Content operations teams, developers, and WeChat Official Account operators use this skill to create WeChat article drafts, upload cover and body images, submit articles for publication, and inspect publish status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send WeChat credentials and unpublished article content to a configured API endpoint.

Mitigation: Keep aws.env out of version control, use the default official WeChat API endpoint when possible, and avoid custom API_BASE or proxy settings unless the endpoint is trusted.

Risk: The release evidence security verdict is suspicious and recommends review before installation.

Mitigation: Install only from trusted configurations and review the skill, environment settings, and intended target account before execution.

Risk: A publish action can move content from a draft workflow to public distribution.

Mitigation: Use draft mode first and require explicit account and article confirmation before any public publish.

## Reference(s):

- [Usage](references/usage.md)
- [Submit Guide](references/submit-guide.md)
- [Pre-Publish Checklist](references/pre-publish-checklist.md)
- [WeChat Official Account API Reference](references/api-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/aiworkskills/skills/aws-wechat-article-publish)
- [WeChat Add Draft API](https://developers.weixin.qq.com/doc/subscription/api/draftbox/draftmanage/api_draft_add)
- [WeChat Free Publish Submit API](https://developers.weixin.qq.com/doc/subscription/api/public/api_freepublish_submit.html)
- [WeChat Add Permanent Material API](https://developers.weixin.qq.com/doc/subscription/api/material/permanent/api_addmaterial.html)
- [WeChat Upload Image API](https://developers.weixin.qq.com/doc/subscription/en/api/material/permanent/api_uploadimage)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce WeChat media_id, publish_id, and status values, and may update article.yaml publication state fields.]

## Skill Version(s):

1.0.24 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
