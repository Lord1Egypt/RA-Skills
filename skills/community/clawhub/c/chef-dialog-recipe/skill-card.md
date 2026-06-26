## Description: <br>
专业厨师对话食谱生成技能：完整的交互式工作流，包含厨师视角生成、AI分析审查、综合优化 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[puppetcat-fire](https://clawhub.ai/user/puppetcat-fire) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to request Chinese dish recipes through a chef-style workflow that prints recipe-generation, review, and optimization steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed scripts print usage and workflow text and may not provide the full advertised recipe-generation workflow locally. <br>
Mitigation: Confirm expected behavior in the reviewed package before relying on generated recipe output. <br>
Risk: Separate external code linked by the artifact may differ from the reviewed package. <br>
Mitigation: Review and scan any separate external code before executing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/puppetcat-fire/chef-dialog-recipe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown, JSON, or plain text recipe guidance; reviewed shell scripts print workflow and usage text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash; the reviewed package does not request credentials or sensitive access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
