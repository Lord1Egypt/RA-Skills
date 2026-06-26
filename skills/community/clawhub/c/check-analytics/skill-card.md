## Description: <br>
Audit existing Google Analytics implementation. Checks for common issues, missing configurations, and optimization opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeftekhari](https://clawhub.ai/user/jeftekhari) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to inspect a project for Google Analytics and related analytics implementations, identify tracking and privacy issues, and produce a prioritized audit report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects repository files for analytics snippets and identifiers. <br>
Mitigation: Use it only in projects where code inspection for analytics configuration is acceptable, and review the generated audit before acting on recommendations. <br>
Risk: Analytics measurement IDs may appear in project code. <br>
Mitigation: Redact sensitive portions of measurement IDs in reports as directed by the artifact. <br>


## Reference(s): <br>
- [Check Analytics on ClawHub](https://clawhub.ai/jeftekhari/check-analytics) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown audit report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Redacts the last six characters of measurement IDs when reporting findings.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
