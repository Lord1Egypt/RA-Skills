## Description:

每日自动搜索过去24小时内的全球和中国重点新闻，并生成一份按主题分类的中文 Markdown 日报。

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to collect recent news across politics, finance, AI, technology, and consumer electronics, then generate a dated Chinese Markdown report for daily review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The weekday scheduled trigger may run automatically when a user expects manual-only news generation.

Mitigation: Review or disable the scheduled weekday trigger before installation if only manual runs are desired.

Risk: Daily news results can still include stale, noisy, or irrelevant items if upstream search results are imperfect.

Mitigation: Review generated reports before relying on them for decisions, especially for time-sensitive finance, policy, or security topics.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown report saved as memory/daily_news_{YYYY-MM-DD}.md]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report is organized by seven news categories and includes a one-sentence daily summary.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
