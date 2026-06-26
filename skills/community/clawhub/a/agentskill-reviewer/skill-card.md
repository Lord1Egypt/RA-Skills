## Description: <br>
Reviews AgentSkill quality and generates professional Markdown reports covering content quality, structure, clarity, token efficiency, and redundancy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ming-shy](https://clawhub.ai/user/ming-shy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to audit AgentSkill documentation, workflow completeness, token efficiency, and structural quality. It can generate Chinese Markdown review reports and optionally use bundled scripts for token counting, report generation, and logic-alignment checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads files from the user-selected target skill directory, so an incorrect target can expose unintended local content to the review process. <br>
Mitigation: Choose the target skill directory deliberately before invoking the review workflow. <br>
Risk: The generated review report may be written to the default skill-reviews/ folder when no output path is specified. <br>
Mitigation: Specify an explicit output path when report location matters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ming-shy/agentskill-reviewer) <br>
- [Publisher Profile](https://clawhub.ai/user/ming-shy) <br>
- [Logic Alignment Validation Guide](references/validation.md) <br>
- [Skill Review Report Template](references/report_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports with optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default report output is a Markdown file under skill-reviews/ unless the user specifies another path.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
