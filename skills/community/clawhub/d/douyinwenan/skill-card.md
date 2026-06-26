## Description: <br>
高中教育内容生产工厂（增强版），用于围绕教育热点生成带有人机协作、数据增强、事实校验和去 AI 味风格约束的抖音口播文案。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[century0327](https://clawhub.ai/user/century0327) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, education marketers, and editorial operators use this skill to produce short-video scripts about high school and education topics. It guides topic selection, data enrichment, hook selection, draft writing, fact-check checkpoints, compliance warnings, and publishing support copy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Education policy, admissions, employment, or exam statistics may be outdated or inaccurate when generated from web search. <br>
Mitigation: Require source review for each cited number, year, policy name, and case detail before publication. <br>
Risk: Short-video copy may include platform-sensitive claims, superlatives, or monetization language. <br>
Mitigation: Run the planned compliance check and have a human editor remove unsupported absolutes, prohibited terms, and misleading claims. <br>
Risk: The strong persona and rhetorical style can overstate advice for students or families. <br>
Mitigation: Keep a human approval step for topic selection, hook choice, final wording, and audience-impact review. <br>
Risk: The workflow references running local commands during review. <br>
Mitigation: Review command behavior before execution and run only the intended tone-check script on user-provided draft text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/century0327/douyinwenan) <br>
- [Publisher profile](https://clawhub.ai/user/century0327) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with Chinese short-video script drafts, hooks, verification notes, compliance warnings, visual suggestions, comment prompts, and inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires human selection at multiple interrupt points and may use web search plus a local tone-check script before publication.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
