## Description:

Checks Chinese contract-fulfillment cost detail tables by recalculating rows, reconciling totals, detecting duplicates and blanks, and citing source text for each finding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Project finance and revenue accounting users at construction, software, and service companies use this skill before monthly revenue and cost recognition or audit workpaper preparation to check whether contract fulfillment cost tables are internally consistent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker can identify accounting-table consistency issues but is not a substitute for accounting judgment, audit procedures, or verification of contracts, invoices, receipts, and business facts.

Mitigation: Use results as a local consistency review aid and have qualified accounting or audit personnel verify conclusions against the underlying records.

Risk: The skill is a Chinese-language local checker for pasted or file-provided table text, so incorrect or incomplete input can limit the reliability of findings.

Mitigation: Provide complete exported table text with required headers and review any insufficient-input messages before relying on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/contract-fulfillment-cost-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [analysis, markdown, shell commands, guidance]

**Output Format:** [Markdown or JSON-formatted local check results, with findings tied to source table text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-provided table text or JSON input; reports insufficient input instead of issuing unsupported conclusions.]

## Skill Version(s):

1.0.20 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
