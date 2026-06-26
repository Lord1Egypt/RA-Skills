## Description: <br>
Analyse une pièce comptable isolée, comme une facture, un relevé bancaire ou une note de frais, pour extraire les données clés et signaler les incohérences sans modifier les fichiers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trendex](https://clawhub.ai/user/trendex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Comptables and accounting operators use this skill to understand one attached accounting document before deciding how to classify or reconcile it. It extracts document type, amounts, VAT, dates, parties, and document-level anomalies, then turns the findings into a concise business summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads accounting PDFs selected by the user, which may contain sensitive financial information. <br>
Mitigation: Use it only on individual documents the user explicitly chooses to analyze and avoid sharing outputs beyond the accounting workflow. <br>
Risk: OCR or visual fallback on scanned or photographed documents can produce uncertain values. <br>
Mitigation: Treat those results as advisory and confirm important amounts, dates, VAT, and parties against the original document. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON from the analysis script, followed by concise human-facing text for the accountant.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only workflow for one user-selected PDF at a time. OCR or visual fallback results should be treated as advisory and confirmed for scanned or photographed documents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
