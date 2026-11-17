## Description:

Analyse une pièce comptable isolée, comme une facture, un relevé bancaire ou une note de frais, pour en extraire les informations clés et signaler les incohérences sans classer, déplacer ni modifier de fichiers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trendex](https://clawhub.ai/user/trendex)

### License/Terms of Use:

MIT-0

## Use Case:

Accountants and finance operators use this skill to understand one accounting document at a time before deciding how to handle it. It extracts document type, amounts, VAT, dates, parties, bank-statement details, and document-level consistency issues, then helps the agent summarize them in concise business language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes sensitive accounting documents, including invoices, bank statements, and expense reports.

Mitigation: Use it only in environments where the agent is authorized to read those local documents and where accounting data handling policies allow local document analysis.

Risk: Scanned or photographed documents may produce lower-confidence visual readings when text extraction is unavailable.

Mitigation: Treat visually read values as subject to confirmation and re-run OCR or manual review for material documents.

Risk: The parsing behavior is primarily tuned for French accounting and banking document formats.

Mitigation: Review extracted fields and anomaly reports carefully before relying on the output for non-French or unusual document layouts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/trendex/skills/analyse-piece-comptable)
- [Publisher profile](https://clawhub.ai/user/trendex)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Concise Markdown summary supported by JSON output from the local analysis script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes one document at a time and is intended to remain read-only.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
