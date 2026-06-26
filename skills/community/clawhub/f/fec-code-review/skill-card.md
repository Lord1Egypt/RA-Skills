## Description: <br>
Use when the user asks for general frontend code review, PR review, merge-readiness assessment, architecture maintainability, type-safety, rendering/state risks, style consistency, testability gaps, or a cross-cutting review summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bovinphang](https://clawhub.ai/user/bovinphang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering reviewers use this skill to review frontend and UI changes for merge readiness, maintainability, type safety, rendering and state risks, style consistency, test gaps, and cross-cutting code quality concerns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The trigger wording is broad and may route general review requests to this frontend-focused workflow. <br>
Mitigation: Invoke it for frontend or UI code review, and use specialized workflows for deep security, accessibility, E2E, or performance investigations. <br>
Risk: Review findings are advisory and may be incomplete when repository context, diffs, or validation output are missing. <br>
Mitigation: Check cited files and lines, run the recommended validation commands, and confirm uncertain findings before blocking a merge. <br>


## Reference(s): <br>
- [Code Review Report Template](references/report-template.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/bovinphang/fec-code-review) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown review report with severity-ranked findings and file/line references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The expected report is saved under reports/code-review-YYYY-MM-DD-HHmmss.md and includes merge guidance, actionable fixes, and explicit uncertainty when more validation is needed.] <br>

## Skill Version(s): <br>
2.5.0 (source: release metadata, package.json, metadata.json, README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
