## Description:

Analyzes ecommerce return records and separates product issues, expectation mismatches, logistics problems, and description issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Operations, merchandising, and customer support teams use this skill to convert return CSV/TSV files, reason text, and product information into reviewable return intelligence. It helps classify causes, identify frequent issues, surface samples needing review, and draft follow-up actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Return records may include customer, order, or other sensitive operational data.

Mitigation: Provide only the local CSV/TSV or text intended for analysis, redact personal data where possible, and prefer dry-run/stdout handling for sensitive inputs.

Risk: The bundled script includes dormant generic audit modes outside the normal returns-analysis workflow.

Mitigation: Use the documented CSV/TSV or text returns-analysis path, and do not modify the bundled spec to enable unused directory or security-audit modes without separate review.

Risk: Draft classifications and recommendations may be incomplete when source data is sparse or ambiguous.

Mitigation: Review the generated cause classifications, high-frequency issues, missing-information list, and follow-up actions before using them for customer service, operations, or product changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/ecommerce-return-intelligence)
- [ClawHub publisher profile](https://clawhub.ai/user/52yuanchangxing)
- [Artifact README](artifact/README.md)
- [Skill specification](artifact/resources/spec.json)
- [Output template](artifact/resources/template.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown report by default; JSON wrapper available from the local script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only local analysis; can write an output file when explicitly requested.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
