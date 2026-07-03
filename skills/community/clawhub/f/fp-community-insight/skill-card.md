## Description: <br>
Analyzes Reddit and professional forum posts from machinery communities, clustering them into weekly hot topics, recurring user pain points, FridayParts content opportunities, and trend signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuxirui677](https://clawhub.ai/user/zhuxirui677) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing and operations teams use this skill to turn machinery-community discussions into Chinese-language topic clusters, pain-point summaries, content ideas, and trend signals for downstream YouTube, blog, and social workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad pain-point or topic-analysis prompts that are not intended for FridayParts machinery-community research. <br>
Mitigation: Use it with explicit Reddit or forum machinery data and confirm the intended FridayParts content workflow before acting on the output. <br>
Risk: Repair, emissions, or aftertreatment topics could produce misleading or noncompliant publishing ideas if not reviewed. <br>
Mitigation: Review outputs before publication, keep DPF/EGR delete discussions limited to lawful maintenance and diagnosis, and require technical validation for repair guidance. <br>
Risk: Small or uneven community samples can make topic clusters and trend signals look more certain than the data supports. <br>
Mitigation: Use representative weekly data when possible and treat trend signals as directional until confirmed by additional community evidence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhuxirui677/skills/fp-community-insight) <br>
- [README](README.md) <br>
- [Example community insight report](examples/example_community_insight.md) <br>
- [Output quality checklist](reference/输出质量checklist.md) <br>
- [GetClawHub import guide](docs/如何导入GetClawHub.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with topic clusters, ranked pain points, content opportunities, trend signals, and compliance notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language output; configured for claude-sonnet-4-6 with temperature 0.6 and max_tokens 2000] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; frontmatter reports 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
