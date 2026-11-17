## Description:

Checks a draft EU VAT return and platform statements for common errors and produces a structured risk report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snowhola](https://clawhub.ai/user/snowhola)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and their advisors can use the skill to review draft VAT return details and platform statements for common issues before consulting a tax representative. It is a preliminary check, not a compliance determination or filing service.

### Deployment Geography for Use:

European Union and United Kingdom, as applicable to the return being reviewed

## Known Risks and Mitigations:

Risk: Submitted VAT and platform records may contain sensitive personal, business, or account information.

Mitigation: Share only records needed for the check and remove unrelated personal or account details.

Risk: The report is preliminary and may not reflect current tax rules or deadlines; passing the check is not a compliance conclusion.

Mitigation: Confirm current rules and deadlines with a tax representative before acting.

## Reference(s):

- [VAT rule table](references/rule-table.md)
- [Filing deadlines](references/deadlines.md)
- [ClawHub skill page](https://clawhub.ai/snowhola/skills/eu-vat-precheck-en)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Structured Markdown risk report with findings, risk levels, supporting basis, recommended actions, and next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pre-check only; does not file returns or generate official filing documents. Marks insufficient information as cannot determine.]

## Skill Version(s):

0.2.0 (source: SKILL.md frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
