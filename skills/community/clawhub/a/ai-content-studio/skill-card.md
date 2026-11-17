## Description:

AI全链路内容工坊 coordinates multi-platform content creation and publishing, covering topic research, article drafting, knowledge-card generation, and public distribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, brand operators, personal-brand builders, and enterprise marketing teams use this skill to turn a topic into WeChat article content, Xiaohongshu copy, knowledge cards, and publishing actions across both platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can publish generated content to public WeChat and Xiaohongshu accounts without a clearly enforced final approval step.

Mitigation: Use draft or preview mode where available, require explicit approval before every live post, and verify connected accounts and credentials before publishing.

Risk: Automated topic research, summarization, and writing can produce inaccurate or misleading public-facing content.

Mitigation: Review claims, sources, images, captions, and hashtags before release, especially for branded or business-critical posts.

Risk: Scheduled or highly automated runs can publish stale or unintended content at scale.

Mitigation: Avoid scheduled runs unless review, approval, monitoring, and rollback procedures are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/skills/ai-content-studio)
- [RSSHub 36Kr feed used for topic research](https://rsshub.app/36kr/posts)
- [Skill README](artifact/README.md)
- [Workflow definition](artifact/workflow.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Images, Links, Shell commands, Guidance]

**Output Format:** [Markdown articles, short-form captions, PNG knowledge cards, platform post URLs, and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured publishing credentials and human review before live WeChat or Xiaohongshu posts.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, workflow.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
