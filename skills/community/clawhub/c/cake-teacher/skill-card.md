## Description: <br>
AI 蛋糕烘焙培训老师，提供蛋糕配方生成、品类教学、步骤指导、翻车诊断、原料替换、装饰技巧、设备推荐、开店指导，并可生成交互式 HTML 教学报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and baking learners use this Chinese-language agent for cake recipes, step-by-step baking instruction, troubleshooting, ingredient substitutions, decorating guidance, equipment selection, and bakery opening guidance. The skill can also generate local HTML teaching reports with recipe cards, timelines, alerts, equipment lists, and diagnosis sections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may generate local HTML teaching reports. <br>
Mitigation: Keep generated reports in a normal output folder and review the chosen output path before running the report command. <br>
Risk: The skill may activate on broad cake-related phrases. <br>
Mitigation: Use explicit prompts when you want the baking tutor behavior, and pause or redirect the agent when a broad trigger is not intended. <br>
Risk: The skill can supplement answers with web search when asked for outside information. <br>
Mitigation: Treat web-search supplements as untrusted unless you explicitly requested current outside information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/cake-teacher) <br>
- [Project homepage](https://github.com/bettermen/cake-teacher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, HTML files, guidance] <br>
**Output Format:** [Chinese-language instructional text and Markdown, with optional shell commands that generate local HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local HTML report files to a user-selected output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
