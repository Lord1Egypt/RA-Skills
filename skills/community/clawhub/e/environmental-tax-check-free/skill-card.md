## Description:

A local Chinese-language checker that recalculates environmental protection tax worksheet rows for pollution-equivalent counts, tax amounts, post-reduction payable amounts, totals, duplicate rows, and missing or invalid fields, with findings tied to source line numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External business, finance, and tax users can run this skill before filing environmental protection tax worksheets to check arithmetic consistency and identify rows that need correction. The skill uses values supplied in the user's worksheet and does not choose local tax rates, pollution-equivalent values, or provide tax advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake arithmetic checks for tax advice or local policy selection.

Mitigation: Use the skill only to recalculate values supplied in the worksheet; have a qualified tax reviewer confirm local rates, pollution-equivalent values, exemptions, and filing positions.

Risk: Incorrect or incomplete worksheet input can produce missing-input results or narrow findings.

Mitigation: Provide the worksheet with headers and relevant rows, review missing-input guidance, and do not treat a passed check as confirmation that emissions data or policy choices are correct.

Risk: Tax worksheet data may be sensitive.

Mitigation: Run the local checker only on files intentionally provided for review and handle those files according to the user's data-protection requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/environmental-tax-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Human-readable console text or JSON result objects with findings, summaries, executed checks, withheld checks, and missing-input guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite worksheet line numbers; the command exits with distinct status codes for success, missing input, unreadable input, and unexpected errors.]

## Skill Version(s):

1.0.50 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
