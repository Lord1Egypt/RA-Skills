## Description:

Generate AWS cost CSVs from a user-provided service list. Use when someone supplies an item list + AWS region and needs per-item pricing plus totals via AWS Price List API or bulk pricing JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crazylion](https://clawhub.ai/user/crazylion)

### License/Terms of Use:


## Use Case:

Developers and cloud engineers use this skill to convert YAML or JSON AWS service item lists into per-item cost CSVs and total estimates. It supports live AWS Price List API lookups and cached or user-supplied bulk pricing JSON for On-Demand and Reserved pricing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use configured AWS CLI credentials and contact AWS pricing services.

Mitigation: Use read-only AWS pricing permissions and prefer bulk or cached pricing data when live API access is not required.

Risk: The skill writes CSV output and cache files based on user-supplied inputs and pricing data.

Mitigation: Write outputs to an expected directory and review generated files before sharing or using them downstream.

Risk: Generated CSV values are not neutralized for spreadsheet formulas when inputs or bulk JSON are not fully trusted.

Mitigation: Treat CSVs as untrusted, inspect suspicious cell values, and sanitize formula-like prefixes before opening in spreadsheet software.

## Reference(s):

- [AWS Pricing Cheat Sheet](references/api_reference.md)
- [AWS Price List API endpoint](https://api.pricing.us-east-1.amazonaws.com/)
- [AWS bulk pricing JSON URL pattern](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/{service}/current/{region}/index.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated CSV contains item rows and a TOTAL row with USD pricing details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
