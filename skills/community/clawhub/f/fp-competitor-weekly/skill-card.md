## Description: <br>
把 Socialinsider 的 IG/TikTok/Facebook CSV 和 Agent-Reach 的 YouTube JSON 合并分析，生成面向 FridayParts 运营团队的竞品社媒周报、图表建议和行动建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuxirui677](https://clawhub.ai/user/zhuxirui677) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
FridayParts operations and content teams use this skill to turn weekly competitor social-media exports into a Chinese Markdown report that highlights growth, engagement, top posts, comment themes, content strategy, visualization ideas, and concrete next actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided competitor exports may contain confidential business data. <br>
Mitigation: Use the skill only in an agent environment where those exports are acceptable to process, and avoid pasting confidential data unless that use is approved. <br>
Risk: Incomplete CSV or JSON fields can lead to missing or misleading weekly-report conclusions. <br>
Mitigation: Review the generated numbers and platform labels against the source exports, and use the included output checklist to confirm that data gaps are called out. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhuxirui677/skills/fp-competitor-weekly) <br>
- [README](README.md) <br>
- [GetClawHub Import Guide](docs/如何导入GetClawHub.md) <br>
- [Example Competitor Weekly Report](examples/example_competitor_weekly.md) <br>
- [Output Quality Checklist](reference/输出质量checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis, Guidance] <br>
**Output Format:** [Chinese Markdown weekly report with ranked findings, chart recommendations, and action items] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only workflow; expects user-provided Socialinsider CSV and Agent-Reach YouTube JSON inputs and does not perform hidden execution or external access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter version 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
