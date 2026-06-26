## Description: <br>
该技能帮助代理为商业培训、企业内训和公开课编写结构化培训大纲，并生成专业排版的 DOCX 文档。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingyw](https://clawhub.ai/user/kingyw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Training consultants, corporate learning teams, and business trainers use this skill to turn a training topic, audience, duration, and customer context into a polished Chinese course outline and DOCX deliverable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create a DOCX file in the workspace or a user-specified path. <br>
Mitigation: Confirm the intended output path and review the generated document before sharing or relying on it. <br>
Risk: The skill may fill in missing training details based on the topic. <br>
Mitigation: Review assumptions in the outline and provide missing audience, duration, customer, or requirement details when accuracy matters. <br>
Risk: Training topics and customer context may include sensitive business information. <br>
Mitigation: Avoid providing confidential business details unless the agent environment is approved for that data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kingyw/cntrain-outline) <br>
- [Training outline structure reference](references/outline-structure.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Structured Chinese training outline with DOCX document output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a DOCX file to a user-specified path or the working directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
