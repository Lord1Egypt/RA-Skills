## Description:

将 Socialinsider 导出的 IG/TikTok/Facebook 竞品 CSV 与 Agent-Reach YouTube 数据合并分析，生成包含排名、Top 内容、评论洞察、图表建议和行动建议的中文运营周报。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuxirui677](https://clawhub.ai/user/zhuxirui677)

### License/Terms of Use:

MIT-0

## Use Case:

FridayParts marketing and operations teams use this skill to turn weekly competitor social-media exports into a decision-ready Chinese competitor report. It helps compare account growth, engagement, top content, comments, content strategy, visualization needs, and next-week actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The report may process social-media export data that was not obtained under the user's organizational authorization, platform terms, or privacy requirements.

Mitigation: Confirm authorization and privacy compliance for Socialinsider exports and Agent-Reach YouTube data before using them as skill inputs.

Risk: Competitor analysis can produce misleading recommendations if required fields such as comments, engagement, views, or platform source labels are missing.

Mitigation: Use the included output checklist and require the report to label missing data rather than filling gaps with unsupported claims.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhuxirui677/skills/fp-competitor-weekly)
- [README.md](artifact/README.md)
- [Import Guide](artifact/docs/如何导入GetClawHub.md)
- [Example Competitor Weekly Report](artifact/examples/example_competitor_weekly.md)
- [Output Quality Checklist](artifact/reference/输出质量checklist.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Chinese Markdown report with ranked sections, bullet insights, chart recommendations, and action recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected to use user-provided Socialinsider CSV data and Agent-Reach YouTube data; configured for concise report generation with max_tokens 2000.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter version 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
