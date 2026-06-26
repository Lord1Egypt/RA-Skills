## Description: <br>
Guides an agent through distinguishing real bugs from change requests, reproducing issues, finding root causes, applying minimal fixes, validating results, and writing bug-fix reports for complex cases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cping6](https://clawhub.ai/user/cping6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill when a reported issue appears to be a defect rather than a feature request. It structures bug triage, reproduction, root-cause analysis, targeted repair, validation, and reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bug-fix reports may capture secrets, personal data, production logs, or screenshots. <br>
Mitigation: Review and redact generated reports before committing or sharing them. <br>
Risk: Debugging and validation tools such as Playwright or Supabase may target the wrong environment. <br>
Mitigation: Confirm tool configuration and target environment before running validation or database checks. <br>
Risk: Proposed fixes can introduce unintended behavior changes. <br>
Mitigation: Review code and documentation diffs, then run relevant tests or browser/database validation before accepting the result. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cping6/bugfix-workflow) <br>
- [Bugfix report template](assets/bugfix-report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, code, shell commands] <br>
**Output Format:** [Text and Markdown; may include code edits, test commands, and a structured bug-fix report for complex issues.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Complex fixes use the bundled bugfix-report-template.md structure.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
