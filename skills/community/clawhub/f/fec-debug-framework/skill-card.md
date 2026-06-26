## Description: <br>
Guides agents through evidence-driven frontend debugging for build failures, runtime errors, UI anomalies, API/data problems, white screens, request failures, and production exceptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bovinphang](https://clawhub.ai/user/bovinphang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and frontend engineers use this skill to classify frontend failures, collect evidence, test root-cause hypotheses, apply minimal fixes, and produce diagnostic reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagnostic reports may contain logs, headers, request bodies, environment details, or other sensitive project information. <br>
Mitigation: Review and redact generated reports before sharing them outside the project team. <br>
Risk: The skill may activate on broad debugging prompts and guide changes before enough evidence is collected. <br>
Mitigation: Confirm the issue type, evidence, and validation results before applying or accepting proposed fixes. <br>


## Reference(s): <br>
- [Diagnostic report template](references/report-template.md) <br>
- [ClawHub skill page](https://clawhub.ai/bovinphang/fec-debug-framework) <br>
- [Frontend Craft repository](https://github.com/bovinphang/frontend-craft) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown diagnostic report with evidence, hypotheses, validation results, and remaining risks; may include code changes and commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are expected at reports/debug-YYYY-MM-DD-HHmmss.md when a diagnostic report is produced.] <br>

## Skill Version(s): <br>
2.5.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
