## Description: <br>
Academic Paper Workflow coordinates a seven-stage academic writing process for research, drafting, citation formatting, integrity checking, peer review, final validation, and journal-ready output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jirboy](https://clawhub.ai/user/jirboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and academic writers use this skill to run a structured paper-production workflow for SCI reviews, experimental papers, grant applications, and research reports. It guides the agent through staged research, writing, citation validation, integrity review, peer review, and submission formatting while preserving human approval checkpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependent academic skills may have their own network access or data handling behavior. <br>
Mitigation: Review and approve each dependent skill before use, especially when working with unpublished manuscripts, citation data, or sensitive research material. <br>
Risk: Workflow checkpoints and passed reports can be mistaken for proof of academic correctness. <br>
Mitigation: Manually verify citations, integrity reports, peer-review results, and final submission files before relying on them for publication or submission. <br>
Risk: Generated drafts or formatted submission files may still contain inaccurate claims, missing disclosures, or journal-specific formatting issues. <br>
Mitigation: Keep the documented human approval checkpoints and perform a final expert review against the target journal requirements before external submission. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jirboy/academic-paper-workflow) <br>
- [Quick start guide](README.md) <br>
- [Workflow stages](references/workflow-stages.md) <br>
- [Skill orchestration guide](references/skill-orchestration.md) <br>
- [Integrity check rules](references/integrity-check-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with command examples, staged checklists, and local workflow validation reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces staged paper artifacts such as research reports, drafts, citation reports, integrity reports, review reports, and submission files when paired with the dependent academic skills.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
