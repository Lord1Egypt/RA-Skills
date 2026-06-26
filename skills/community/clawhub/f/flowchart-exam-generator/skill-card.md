## Description: <br>
Generates Chinese single-choice and multiple-choice exam questions from an uploaded flowchart and exports them as a structured Excel question bank. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geming416684729-svg](https://clawhub.ai/user/geming416684729-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, educators, and training-content authors use this skill to turn flowchart images into review-ready exam questions with answers, explanations, and source labels. It is suited for generating “应知应会” question banks from operational process diagrams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated questions or explanations may misread unclear flowchart content. <br>
Mitigation: Review the generated question bank against the source flowchart before sharing or importing it into training systems. <br>
Risk: The Excel output path determines where generated files are written. <br>
Mitigation: Choose the output filename and directory intentionally, especially when running in shared workspaces. <br>
Risk: The helper script depends on the local Python package environment. <br>
Mitigation: Run it in a trusted Python environment with the expected openpyxl dependency installed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/geming416684729-svg/flowchart-exam-generator) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/geming416684729-svg) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, files] <br>
**Output Format:** [Excel workbook with generated exam questions, answers, explanations, and source labels] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses four options per question and numeric answer encoding where A=1, B=2, C=3, and D=4.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
