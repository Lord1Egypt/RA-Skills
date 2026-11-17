## Description:

Chinese-language agent skill that conducts conversational enterprise legal risk screening across 13 compliance modules and returns risk scores and remediation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lswjp1234-lgtm](https://clawhub.ai/user/lswjp1234-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

External business users and legal or compliance operators use this skill to run Chinese-language enterprise legal-risk screening, identify top risk areas, and receive remediation guidance. The skill supports a free quick screen and paid follow-up flows for module-specific analysis or a fuller report.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The workflow can solicit sensitive company, tax, invoice, employment, and possible criminal-exposure details.

Mitigation: Use sanitized or minimal facts unless the publisher is trusted and data-handling expectations are clear.

Risk: The skill routes users to paid legal-service steps and may request payment screenshots.

Mitigation: Treat payment and lawyer-contact steps as off-platform promotional activity, and verify payment handling and representation terms independently.

Risk: Outputs may be mistaken for formal legal advice.

Mitigation: Use the screening as informational guidance and consult a qualified lawyer before relying on it for legal decisions.

## Reference(s):

- [13模块97+检测项完整题库](artifact/references/modules.md)
- [ClawHub skill listing](https://clawhub.ai/lswjp1234-lgtm/skills/enterprise-law-risk-checker)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Conversational Markdown with questionnaires, risk scores, ranked risk points, and remediation suggestions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Informational legal-risk screening only; paid flows may request payment screenshots and follow-up contact.]

## Skill Version(s):

1.0.0 (source: server release metadata and README version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
