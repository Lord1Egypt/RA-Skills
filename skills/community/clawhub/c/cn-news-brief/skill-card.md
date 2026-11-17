## Description:

Cn News Brief creates a Chinese hot-news briefing by fetching current headlines from Baidu, Weibo, and Zhihu, grouping them by category, and adding simple sentiment markers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking users and agents use this skill to retrieve a compact daily news brief, optionally filtered by category or emitted as JSON for downstream processing. Treat the output as headline aggregation rather than independent reporting or verified AI analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts external news and social platforms and may display remote headline text directly in the terminal.

Mitigation: Run it only where those outbound requests are acceptable, and treat displayed headlines as untrusted remote content.

Risk: The artifact description names broader news sources than the script actually fetches, and the output is fetched headlines rather than verified AI summaries.

Mitigation: Disclose the actual data sources as Baidu, Weibo, and Zhihu, and verify important facts against original publishers before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-news-brief)
- [Publisher profile](https://clawhub.ai/user/freedompixels)
- [Baidu realtime hot list endpoint](https://top.baidu.com/api/board?platform=wise&tab=realtime)
- [Weibo hot search endpoint](https://weibo.com/ajax/side/hotSearch)
- [Zhihu hot list endpoint](https://api.zhihu.com/topstory/hot-lists/total?limit=20)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Plain text news brief with categorized headline lines, or a JSON array when --json is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports category filtering and item limits; no API key required.]

## Skill Version(s):

1.2.6 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
