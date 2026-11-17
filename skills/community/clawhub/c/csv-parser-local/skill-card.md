## Description:

Parse and generate RFC 4180 compliant CSV that works across tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panchenbo](https://clawhub.ai/user/panchenbo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill for guidance on parsing, validating, and generating CSV data that remains compatible across common tools and spreadsheet workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated CSV values can trigger spreadsheet formula behavior when opened in spreadsheet tools.

Mitigation: Review generated CSVs and escape fields that start with =, +, -, or @ before opening them in spreadsheet applications.

Risk: CSV data can be misread when delimiter, quoting, encoding, locale, or long-number handling differs between tools.

Mitigation: Validate delimiter, quoting, encoding, column counts, date formats, and long numeric identifiers before relying on parsed or generated CSV output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/panchenbo/skills/csv-parser-local)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown guidance with inline examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No installers, persistence, or hidden behavior are identified in the security evidence.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
