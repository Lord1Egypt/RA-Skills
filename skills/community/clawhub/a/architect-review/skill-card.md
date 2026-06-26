## Description: <br>
Reviews project architecture against OpenSpec documents and source structure, producing scored findings and actionable recommendations across configurable dimensions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fdingiit](https://clawhub.ai/user/fdingiit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to evaluate module and component architecture against OpenSpec requirements and project code before major implementation, refactoring, or design review work. It supports spec-only and incremental reviews and helps triage issues into a structured Markdown report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads project specifications and architecture-relevant source files, which may include sensitive design details. <br>
Mitigation: Install and run it only in projects where the agent is allowed to inspect those files. <br>
Risk: The generated report may influence later implementation or automated fix work. <br>
Mitigation: Review the report, including its metadata block, before sharing it or using it to drive follow-up changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fdingiit/architect-review) <br>
- [Architecture Review Dimensions](artifact/dimensions.md) <br>
- [Architecture Review Examples](artifact/examples.md) <br>
- [Architecture Review Report Template](artifact/report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown architecture review report with tables, scoring, recommendations, and machine-readable metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a local .arch-review/{date}-report.md file after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
