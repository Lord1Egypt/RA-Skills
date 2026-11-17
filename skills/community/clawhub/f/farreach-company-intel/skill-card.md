## Description:

This skill guides an agent through company intelligence gathering, contact discovery, email validation, and local or OKKI record creation from a company URL or name.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjboy007](https://clawhub.ai/user/cjboy007)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and business-development users can use this skill to research target companies, identify relevant business contacts, validate contact information, and prepare structured local and OKKI records. It should be used only for authorized, policy-compliant business contact research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Business contact data may be collected, verified, and stored without adequate authorization or retention controls.

Mitigation: Use only on scoped, authorized company targets and define compliance and retention requirements before collection.

Risk: Inferred email generation and raw SMTP probing can create privacy, compliance, or deliverability risk.

Mitigation: Disable inferred email generation and raw SMTP probing unless the user explicitly approves the target scope and validation method.

Risk: Automatic OKKI or CRM writes can persist incorrect or unauthorized records.

Mitigation: Require user approval and human review before creating or updating CRM records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cjboy007/skills/farreach-company-intel)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown dossier, structured contact records, and inline shell or Python command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local files and OKKI CRM records when explicitly authorized.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
