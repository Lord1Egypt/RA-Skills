## Description:

Extracts tables and key fields from Chinese business documents, attaches source locations, and reports validation issues in structured records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tingyun01](https://clawhub.ai/user/tingyun01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data teams use this skill to extract and validate structured records from Chinese business documents such as invoices, statements, policies, and spreadsheets. It reports missing or malformed fields and preserves source locations for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Extracted values or cited locations may be inaccurate, and the scripts do not include built-in OCR.

Mitigation: Check each value and its cited source location against the original document, including when validation passes.

Risk: Generated records may contain personal data.

Mitigation: Mask personal data before sharing records and protect generated records as carefully as the source documents.

Risk: Unreviewed installation sources may introduce supply-chain risk.

Mitigation: Use reviewed local files or pin installation sources.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/tingyun01/skills/cn-doc-table-extract)
- [Chinese document field library](references/chinese-document-field-library.md)
- [Table extraction traps](references/table-extraction-traps.md)
- [Pre-delivery acceptance checklist](references/delivery-acceptance-checklist.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Structured data, Guidance]

**Output Format:** [Markdown tables and validation report, plus JSON records with field-level source citations or unverified markers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports missing fields and validation issues; values are not silently repaired.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
