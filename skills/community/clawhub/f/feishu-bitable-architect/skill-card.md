## Description: <br>
Helps users translate business workflows into Feishu Bitable table designs with diagnostic questions, field planning, relationship design, views, and automation suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shianaixuexi-cell](https://clawhub.ai/user/shianaixuexi-cell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and operators use this skill when they need a Feishu Bitable structure for customer management, content operations, project tracking, order management, hiring, personal knowledge, or another business workflow. The skill asks clarifying questions before producing an implementation-ready schema plan for a separate Feishu table-building agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger examples can activate the skill for vague business-management requests. <br>
Mitigation: Confirm that the user wants a Feishu Bitable design before producing or handing off a schema plan. <br>
Risk: A downstream table-building agent could turn an unsuitable schema, field type, relationship, or automation suggestion into workspace changes. <br>
Mitigation: Review the proposed fields, relationships, views, automations, and creation step before allowing another agent to build tables. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shianaixuexi-cell/feishu-bitable-architect) <br>
- [business-templates.md](artifact/references/business-templates.md) <br>
- [common-patterns.md](artifact/references/common-patterns.md) <br>
- [field-types-guide.md](artifact/references/field-types-guide.md) <br>
- [validation-rules.md](artifact/references/validation-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown table-structure plan with field lists, relationships, views, automation suggestions, and risk notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Does not call Feishu APIs or create tables directly; outputs a plan for review and downstream execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
