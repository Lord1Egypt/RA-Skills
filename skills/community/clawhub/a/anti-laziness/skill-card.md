## Description: <br>
Anti-Laziness Protocol gives an agent evidence-first checklists for source-code review, technical research, report writing, and document validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[augsh](https://clawhub.ai/user/augsh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, reviewers, and technical writers use this skill to keep agent work grounded in concrete evidence, source references, explicit confidence labels, and task-specific self-checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may apply a strict evidence-first process broadly, which can make lightweight analysis slower or more rigid. <br>
Mitigation: Use it when the task benefits from verification, source review, or formal quality checks, and state any scope or depth limits up front. <br>
Risk: The artifact guidance may steer the agent toward Chinese-language conventions or temporary progress notes. <br>
Mitigation: Keep the response language aligned with the user and create temporary notes only when the environment and task call for them. <br>


## Reference(s): <br>
- [Anti-Laziness Protocol](SKILL.md) <br>
- [Writing guidelines](references/写作规范.md) <br>
- [Validation guidelines](references/校验规范.md) <br>
- [Source research guidelines](references/源码规范.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance, checklists, evidence tables, and review notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request file and line references, confidence labels, progress notes, and independent review for high-rigor tasks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
