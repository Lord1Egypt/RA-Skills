## Description:

Checks user-provided Canadian sales data and platform statements for common GST/HST, QST/PST, registration, filing, and invoicing issues, then returns a structured pre-check report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snowhola](https://clawhub.ai/user/snowhola)

### License/Terms of Use:

MIT-0

## Use Case:

External cross-border sellers use the skill to review Canadian sales-tax records for common GST/HST, QST/PST, marketplace coverage, registration, filing-frequency, currency, and invoice issues before consulting a tax professional.

### Deployment Geography for Use:

Canada

## Known Risks and Mitigations:

Risk: A preliminary check based on incomplete information or simplified tax references could miss an obligation or give an inaccurate view of a seller’s position.

Mitigation: Treat the report as a pre-check, not a compliance conclusion; verify current rules and deadlines with official tax authorities or a Canadian tax advisor before acting.

Risk: Sales records or platform statements may include unnecessary customer or account details.

Mitigation: Share only the sales information needed for the check and redact unnecessary customer or account details.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/snowhola/skills/canada-gst-hst-precheck)
- [Filing deadlines reference](artifact/references/deadlines.md)
- [Canadian GST/HST rule table](artifact/references/rule-table.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Structured Markdown risk summary and findings table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preliminary assessment from user-provided information; missing details are marked as undetermined.]

## Skill Version(s):

0.1.0 (source: frontmatter; server-resolved release 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
