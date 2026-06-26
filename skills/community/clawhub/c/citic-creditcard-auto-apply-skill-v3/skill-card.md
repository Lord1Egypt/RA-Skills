## Description: <br>
Recommends CITIC Bank credit cards from official CITIC pages and helps an agent prefill official application forms with confirmed user data, stopping before final submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lgmsmile](https://clawhub.ai/user/lgmsmile) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to compare CITIC credit-card options and guide an agent through official-site prefill after they confirm each field. It is intended to keep recommendation, candidate-data review, and final human submission separate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect and save sensitive applicant details locally. <br>
Mitigation: Use a dedicated workspace, avoid adding unnecessary personal data to memory files, and delete candidate or application-plan outputs after use. <br>
Risk: Generated prefill data may include stale, incorrect, or unconfirmed applicant details. <br>
Mitigation: Inspect generated JSON before browser prefill and confirm each field with the applicant before it is used. <br>
Risk: Credit-card application steps can include OTP, authorization, agreement, and final-submission actions that require the applicant's direct control. <br>
Mitigation: Have the applicant personally handle OTP, authorization, agreement checkboxes, and final submission. <br>


## Reference(s): <br>
- [CITIC Credit Card Homepage](https://creditcard.ecitic.com/) <br>
- [Browser Prefill Workflow](docs/browser_workflow.md) <br>
- [Security and Compliance Notes](docs/security_notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown recommendations and JSON prefill plans with inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before prefill and stops before OTP, authorization, agreement checkboxes, and final submission.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata; artifact frontmatter lists 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
