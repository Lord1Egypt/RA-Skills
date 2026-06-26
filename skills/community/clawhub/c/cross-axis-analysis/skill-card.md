## Description: <br>
横纵分析法 helps agents produce research reports by combining longitudinal timeline analysis with cross-sectional competitive comparison. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zcz-user](https://clawhub.ai/user/zcz-user) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, students, strategists, and other external users use this skill to structure deep or quick research on an unfamiliar product, company, technology, person, or trend. It guides an agent to compare a subject's historical development with its current competitive landscape and then synthesize the intersection into a report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research targets may contain confidential material that could be sent to an external AI service when the filled prompt is executed. <br>
Mitigation: Avoid including confidential or sensitive information in the research target unless the chosen AI service and deployment environment are approved for that data. <br>
Risk: The skill can activate on broad research prompts and may produce incorrect or misleading analysis if the downstream model has weak retrieval or reasoning for the topic. <br>
Mitigation: Review the generated report, verify important claims against reliable sources, and supplement cold or niche domains with manual research. <br>


## Reference(s): <br>
- [横纵分析法 prompt template](references/prompt-template.md) <br>
- [ClawHub skill page](https://clawhub.ai/zcz-user/cross-axis-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/zcz-user) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown research report or concise markdown bullet summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports a long-form report mode around 10,000-30,000 Chinese characters and a quick mode capped at 1,500 Chinese characters.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
