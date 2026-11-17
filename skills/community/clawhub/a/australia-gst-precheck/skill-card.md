## Description:

Pre-check Australian GST and BAS information for common classification, registration, marketplace, filing, export-evidence, and price-display risks, then produce a structured risk report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snowhola](https://clawhub.ai/user/snowhola)

### License/Terms of Use:

MIT-0

## Use Case:

External cross-border sellers use the skill to pre-screen Australian GST and draft BAS information, identify common issues, and prepare questions or records for a registered tax or BAS agent. It does not lodge returns or make compliance determinations.

### Deployment Geography for Use:

Australia

## Known Risks and Mitigations:

Risk: Draft BAS data and platform statements may contain sensitive financial or customer information.

Mitigation: Share only the information needed for the pre-check and redact unrelated customer or account details.

Risk: Simplified GST rules or incomplete facts may lead to an incorrect filing, registration, or classification decision.

Mitigation: Treat the report as a pre-check and confirm applicable rules and filing or registration decisions with a registered tax or BAS agent.

## Reference(s):

- [GST rule table](references/rule-table.md)
- [BAS filing deadlines](references/deadlines.md)
- [ClawHub skill page](https://clawhub.ai/snowhola/skills/australia-gst-precheck)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Structured Markdown risk report with a summary, findings table, and prioritized next steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flags missing information as cannot determine; pre-check only, not an official return or compliance conclusion.]

## Skill Version(s):

0.1.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
