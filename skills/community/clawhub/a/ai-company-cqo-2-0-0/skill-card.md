## Description: <br>
Provides an AI company Chief Quality Officer workflow for end-to-end quality inspection, PDCA-BROKE improvement loops, G0-G4 quality gates, multi-level review, and meta-prompt optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnsmithfan](https://clawhub.ai/user/johnsmithfan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Quality, governance, and agent-operations teams use this skill to structure AI quality assurance workflows, quality-gate decisions, defect reporting, and continuous improvement plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation may route unrelated quality or governance prompts into this skill. <br>
Mitigation: Use explicit prompts that name the intended CQO workflow, language, and quality-governance scope. <br>
Risk: Subagent or session workflows may expose sensitive project context if used with confidential inputs. <br>
Mitigation: Avoid sharing sensitive project data with subagent or session workflows unless that exposure is acceptable. <br>
Risk: The bundled checker writes a report file into the checked skill directory. <br>
Mitigation: Run the checker only on intended skill directories and review generated reports before committing or publishing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johnsmithfan/ai-company-cqo-2-0-0) <br>
- [ClawHub metadata homepage](https://clawhub.com/skills/ai-company-cqo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured quality-governance guidance, with optional code or shell commands for local quality-gate checks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce quality assessments, defect reports, improvement plans, review decisions, and local checker reports.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata; artifact frontmatter says 2.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
