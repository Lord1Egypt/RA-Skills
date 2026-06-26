## Description: <br>
Multi-dimensional code audit using structured subagent delegation for GitHub releases, pull requests, and codebases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinghaojia](https://clawhub.ai/user/yinghaojia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit releases, pull requests, or codebases across security, concurrency, implementation logic, test quality, and simplicity concerns. It guides structured subagent review and synthesizes findings into severity and priority matrices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read or fetch many source files and share repository context with subagents during review. <br>
Mitigation: Use it only on repositories, pull requests, or releases that the operator is authorized to share with the agent and subagents. <br>
Risk: Deep multi-agent audits can consume extra model and tool resources. <br>
Mitigation: Choose audit depth based on repository size and review criticality, and reserve Four-Eyes verification for critical or uncertain findings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinghaojia/deep-code-review) <br>
- [Audit Dimensions](references/audit-dimensions.md) <br>
- [Four-Eyes Cross-Verification Protocol](references/four-eyes.md) <br>
- [Output Format Specification](references/output-format.md) <br>
- [Severity Classification Rubric](references/severity-rubric.md) <br>
- [Subagent Audit Templates](references/subagent-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown audit report with structured findings, source citations, severity tables, priority matrix, and executive summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include subagent reports, Confirmed/Mitigated/False Alarm conclusions, Four-Eyes verification notes for critical findings, and a simplicity score.] <br>

## Skill Version(s): <br>
1.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
