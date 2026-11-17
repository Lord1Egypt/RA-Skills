## Description:

每日热榜技能用于查询微博、知乎、B站、抖音等54个平台的热榜数据，并支持分类浏览、历史保存、跨平台聚合和舆情监控。

This skill is ready for commercial/non-commercial use.

## Publisher:

[one-box-u](https://clawhub.ai/user/one-box-u)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to retrieve and summarize trending topics from supported news, social, video, technology, gaming, reading, and utility platforms. It can also help users browse platform categories, save local history, configure personalized topic preferences, and monitor keywords for high-interest events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release installs mutable Python dependencies.

Mitigation: Install in an isolated, low-privilege environment and pin dependency versions and hashes before deployment.

Risk: The skill stores local hot-list history and security evidence flags unsafe path handling.

Mitigation: Disable or tightly scope auto-save when history retention is not required, and restrict storage APIs to validated source IDs and dates.

Risk: The package claims scheduled Feishu pushes without documented consent, recipient confirmation, cancellation, or data-content controls.

Mitigation: Treat scheduled pushes as under-specified until explicit opt-in, recipient validation, cancellation, and content-review controls are documented.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/one-box-u/skills/daily-hot-news)
- [DailyHotApi](https://github.com/imsyy/DailyHotApi)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-formatted text with occasional JSON-like data summaries and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include hot-list rankings, platform categories, saved-history summaries, monitoring configuration responses, and installation or runtime guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
