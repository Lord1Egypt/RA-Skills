## Description:

Helps an agent search, summarize, and compare public Bilibili video, article, livestream, creator, and ranking-page information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to organize public Bilibili trends, keyword results, creator performance, and ranking-page metrics into concise summaries for lightweight analysis and reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests could expand into bulk scraping or download-oriented workflows.

Mitigation: Keep tasks specific, limit page scope, avoid downloads, and do not use the skill for batch collection.

Risk: Optional login-state context can include personal-page information.

Mitigation: Use login state only when intentionally organizing personal-page information and avoid automated interactions.

Risk: Dynamic rendering or verification challenges can make extracted Bilibili data incomplete or stale.

Mitigation: Open pages manually when needed, verify important metrics against the public page, and treat summaries as lightweight analysis.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/codekungfu/skills/bilibili-hot-trend)
- [Bilibili](https://www.bilibili.com/)
- [Bilibili Rankings](https://www.bilibili.com/v/popular/rank)
- [Bilibili Search](https://search.bilibili.com/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summaries and guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on public-page summaries and comparisons; does not provide downloading, reverse engineering, or bulk collection workflows.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
