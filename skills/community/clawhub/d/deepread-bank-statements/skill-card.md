## Description: <br>
Extracts structured JSON from PDF or scanned bank statements, including account details, statement periods, balances, transactions, and per-field review flags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uday390](https://clawhub.ai/user/uday390) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to submit bank statement documents to DeepRead, retrieve typed extraction results, and reconcile transactions against opening and closing balances. It is suited for lending, underwriting, bookkeeping, personal finance, cash-flow analysis, audit, and forensics workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive bank statements and sends documents to the DeepRead API for processing. <br>
Mitigation: Use it only for documents intended for DeepRead processing, follow applicable privacy requirements, and redact PII before external sharing. <br>
Risk: The skill requires a DeepRead API key. <br>
Mitigation: Store DEEPREAD_API_KEY securely, avoid committing it to files, and rotate it if exposed. <br>
Risk: Extracted transactions or balances may need review before downstream financial decisions. <br>
Mitigation: Check per-field needs_review flags and reconcile opening balance plus transactions against the closing balance. <br>


## Reference(s): <br>
- [DeepRead Bank Statements on ClawHub](https://clawhub.ai/uday390/deepread-bank-statements) <br>
- [DeepRead homepage](https://www.deepread.tech) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with JSON schemas, Python and cURL examples, and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DEEPREAD_API_KEY and posts documents to https://api.deepread.tech for processing.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
