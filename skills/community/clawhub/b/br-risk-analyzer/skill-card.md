## Description: <br>
Analyzes code changes against requirement documents to identify, prioritize, and report evidence-based code risk findings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhijialin](https://clawhub.ai/user/zhijialin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to compare scoped code changes with requirement or design documents and produce prioritized risk findings, requirement coverage notes, and optional test recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect repository source code and requirement documents, which may include confidential implementation or business details. <br>
Mitigation: Use it only in repositories where that access is acceptable, and provide explicit paths, branches, and scope limits before analysis. <br>
Risk: Generated risk reports and project-understanding notes may retain sensitive project details. <br>
Mitigation: Review or delete generated reports and artifact/resources/project-understanding.md when working with confidential code. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhijialin/br-risk-analyzer) <br>
- [README](artifact/README.md) <br>
- [Project understanding notes](artifact/resources/project-understanding.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown risk report with summary, priority tables, coverage assessment, and optional testing recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save generated risk reports and project-understanding notes in the workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
