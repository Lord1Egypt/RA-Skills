## Description: <br>
Generates standardized Word design documents from front-end and back-end code plus front-end pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superchao9](https://clawhub.ai/user/superchao9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn application module code and page captures into structured module design documentation, including flow descriptions, screenshots, data-table schemas, and implementation class listings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask for application login credentials to capture authenticated front-end pages. <br>
Mitigation: Use a temporary or least-privileged test account, and do not share production passwords in chat. <br>
Risk: Generated screenshots, notes, and Word documents may contain authenticated UI views or internal design details. <br>
Mitigation: Review and redact screenshots and generated documents before storing or distributing them. <br>
Risk: The skill reads front-end and back-end source code as part of its documentation workflow. <br>
Mitigation: Run it only on codebases that the agent and operator are authorized to inspect. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/superchao9/design-doc-generator) <br>
- [Design document format specification](artifact/references/doc-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Code, Screenshots, Guidance] <br>
**Output Format:** [Markdown notes, PNG screenshots, Python code, and a Word .docx design document] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a workspace output directory containing design notes, screenshots, and the generated Word document.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
