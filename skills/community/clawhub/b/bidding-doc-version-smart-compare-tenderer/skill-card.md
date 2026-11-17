## Description:

Compares old and revised bidding documents for procuring entities, flags change impacts and compliance risks, and produces a pre-release self-check report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

Procuring entities, purchasers, and procurement agencies use this skill to compare two bidding-document versions before issuing corrections or addenda. It helps prioritize changes that need compliance review, deadline handling, clarification, or internal release approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may append publisher attribution to ordinary chat responses without user opt-in.

Mitigation: Review and remove or override the signature convention before installation if unsolicited attribution is not acceptable.

Risk: Tender documents may contain sensitive procurement information, and the skill discloses an IMA knowledge-base lookup.

Mitigation: Use only approved environments and confirm connector and data-handling policies before processing confidential bidding materials.

Risk: Scanned PDFs, very large files, complex tables, or unusual layouts can produce incomplete extraction or lower-confidence analysis.

Mitigation: Require review of data-quality warnings and source documents before relying on the report for publication decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/bidding-doc-version-smart-compare-tenderer)
- [Output Schema](artifact/references/output_schema.md)
- [Stage 3 Diff Rules](artifact/references/stage3_diff.md)
- [Stage 4 Classification](artifact/references/stage4_classify.md)
- [Stage 5 Review](artifact/references/stage5_review.md)
- [Golden Regression Set](artifact/references/golden_longling_4vs5.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and DOCX reports with JSON intermediate files and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analyzes two uploaded DOCX or PDF bidding documents and includes data-quality warnings when extraction is incomplete.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact manifest and _meta list 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
