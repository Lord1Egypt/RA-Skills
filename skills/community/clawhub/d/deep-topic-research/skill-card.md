## Description: <br>
对用户提出的具体话题/课题/行业进行深度调研，输出结构化报告。结合多智能体并行搜索（借鉴女娲Nuwa）和克制调用原则（借鉴AutoGLM DeepResearch），先展示中间发现再决策。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realpda](https://clawhub.ai/user/realpda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and employees use this skill to guide deep research on a specific topic, market, industry, or question. The skill structures the work into scoped research dimensions, interim findings, source review, synthesis, and actionable recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research outputs can be incomplete, outdated, or overly dependent on weak sources if the agent stops before checking enough evidence. <br>
Mitigation: Use the skill's interim findings, source weighting, citation requirements, and quality self-check before treating conclusions as decision support. <br>
Risk: The workflow may require browsing or delegated search across external sources selected during use. <br>
Mitigation: Review source choices, avoid excluded low-reliability platforms, and confirm important claims against authoritative sources before acting on the report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/realpda/deep-topic-research) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown research reports with interim finding summaries, cited source lists, and actionable recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include research scope confirmation, 2-4 search dimensions, source quality notes, risk/challenge analysis, and optional Obsidian note content when requested by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
