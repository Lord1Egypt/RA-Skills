## Description: <br>
设计走查将生成的 HTML/CSS 页面与用户提供的设计规范文档逐项对照，并输出结构化合规报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asz2864](https://clawhub.ai/user/asz2864) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers use this skill to review generated HTML/CSS pages against a Markdown design specification and receive prioritized compliance findings with repair guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The review requires reading design specifications and page/CSS files, so unintended file paths could expose sensitive project details. <br>
Mitigation: Provide only the intended Markdown specification and target HTML/CSS files, and confirm paths before running the review. <br>
Risk: Generated repair suggestions may be incomplete when the design specification or CSS structure is ambiguous. <br>
Mitigation: Treat the report as review guidance and verify proposed CSS changes before applying them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Guidance] <br>
**Output Format:** [Markdown report with tables and CSS code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes compliance counts, prioritized findings, pass items, and repair suggestions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
