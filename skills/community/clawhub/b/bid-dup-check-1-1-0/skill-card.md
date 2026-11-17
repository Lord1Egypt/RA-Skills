## Description:

Screens Chinese tender and bidding documents for duplicate text, key-information collisions, document metadata parity, table similarity, and two-file diffs, then produces structured preliminary risk reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

External procurement teams, bidders, and reviewers use this skill to run preliminary duplication and bid-collusion risk screening on Chinese .docx, text-layer .pdf, and .txt tender documents. It supports self-checks and initial screening, not formal committee decisions or legal determinations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes procurement documents that may contain sensitive bid data, personal data, and commercial information.

Mitigation: Use it only with documents the operator is authorized to process, review generated JSON/Markdown/DOCX outputs before sharing, and clean extracted files and images from the workspace after use.

Risk: Generated findings are preliminary and may be incorrect, incomplete, or misleading in high-stakes procurement decisions.

Mitigation: Treat reports as screening support only and require qualified human review before any formal bid evaluation, complaint, penalty, or legal decision.

Risk: Reports include a fixed author and WeChat feedback footer.

Mitigation: Review the generated report footer before distribution and modify the skill or report output when that attribution is not appropriate.

Risk: Scanned PDFs, image-only content, and missing tender baselines can reduce coverage or increase false positives.

Mitigation: Prefer text-layer PDFs or DOCX/TXT files, enable OCR only when available and authorized, and provide tender documents for baseline exclusion when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/bid-dup-check-1-1-0)
- [Detection rules reference](artifact/references/detection_rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, DOCX, and structured JSON findings with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces extracted document JSON, findings JSON, Markdown reports, DOCX reports, risk summaries, limitations, and follow-up guidance.]

## Skill Version(s):

1.1.0 (source: artifact frontmatter and manifest; ClawHub release metadata version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
