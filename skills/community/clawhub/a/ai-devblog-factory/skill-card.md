## Description:

AI DevBlog Factory gathers GitHub Trending projects and developer news, analyzes trends, generates a structured technical report, and can publish it to Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical teams use this skill to automate tracking open-source and developer-news trends, turn the results into a readable weekly report, and optionally publish the report to Feishu for team knowledge sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may be published to Feishu with permissions that are broader than intended.

Mitigation: Review Feishu permissions before installing, use draft mode or require explicit approval before publishing, and limit the Feishu bot to the intended folder.

Risk: AI-generated trend analysis can be incomplete or misleading when used as team knowledge material.

Mitigation: Review generated reports before broad distribution and keep source links available for verification.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/skills/ai-devblog-factory)
- [dev.to RSS feed](https://dev.to/feed)
- [Hacker News RSS feed](https://news.ycombinator.com/rss)

## Skill Output:

**Output Type(s):** [markdown, text, configuration]

**Output Format:** [Markdown report with structured analysis text and Feishu document metadata when publishing is enabled]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can run in draft mode without publishing; otherwise may return Feishu document URL and document ID.]

## Skill Version(s):

1.0.0 (source: server release metadata and workflow.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
