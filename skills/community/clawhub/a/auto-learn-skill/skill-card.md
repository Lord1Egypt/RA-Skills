## Description: <br>
自动学习技能从对话中提取可复用知识，并帮助创建或更新持久化技能供 Agent 后续使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users and skill authors use this skill to identify repeated conversation patterns, capture useful workflows, and turn recurring solutions into reusable skills. It is intended for teams that want an agent to accumulate knowledge across interactions while preserving human review over learned content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read recent conversations and generate persistent skills, which may capture sensitive information or unsafe instructions. <br>
Mitigation: Require manual approval before scanning history or writing files, and review generated skill content before installing or sharing it. <br>
Risk: Automatically learned skills may preserve incorrect, outdated, or over-generalized guidance. <br>
Mitigation: Keep learned skills in a bounded location with an easy rollback path, and validate generated guidance against the original task context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/auto-learn-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown skill content and file creation or update guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated skills should be reviewed for sensitive data, unsafe instructions, and accuracy before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
