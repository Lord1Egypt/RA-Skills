## Description:

每日抓取全球AI新闻，自动深度研究，生成高质量公众号长文并发布至微信和小红书.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, AI industry practitioners, researchers, and personal-brand operators use this skill to gather daily AI news, research cross-platform reactions, draft a long-form WeChat article, generate a cover image, and publish adapted content to WeChat and Xiaohongshu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may post generated AI-news content to connected WeChat and Xiaohongshu accounts without a clearly enforced approval gate.

Mitigation: Use draft-only defaults and require explicit per-platform confirmation before any scheduled or manual publication.

Risk: Generated articles, summaries, and cover images may contain inaccurate, outdated, or misleading claims from news and social sources.

Mitigation: Review source links, article text, image content, and platform-specific captions before publishing.

Risk: A scheduled run could publish to the wrong destination account or with changed dependency behavior.

Mitigation: Confirm destination accounts before each publication and pin dependency versions for the component skills used by the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/skills/2026-04-19)
- [Publisher profile](https://clawhub.ai/user/zlszhonglongshen)
- [Artifact README](artifact/README.md)
- [Workflow definition](artifact/workflow.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Images, Links, Guidance]

**Output Format:** [Markdown article, text summaries, generated cover image, and platform publication result links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a daily AI news summary, research report, 3000-5000 word WeChat article, 900x383 cover image, and WeChat/Xiaohongshu publication results.]

## Skill Version(s):

1.0.0 (source: server release metadata and workflow.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
