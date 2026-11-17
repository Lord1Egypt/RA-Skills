## Description:

Extracts structured JSON from PDF or scanned bank statements, including account details, statement periods, balances, transactions, confidence flags, and PII redaction guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uday390](https://clawhub.ai/user/uday390)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operations teams use this skill to extract typed, reviewable transaction data from bank statements for underwriting, bookkeeping, cash-flow analysis, audits, and personal finance workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bank statements can contain sensitive financial data and personally identifiable information.

Mitigation: Use test or redacted documents where possible, confirm authorization before upload, and review DeepRead privacy, retention, and compliance terms before processing real statements.

Risk: The skill requires an API key for DeepRead.

Mitigation: Store DEEPREAD_API_KEY securely, avoid sharing it in prompts or logs, and rotate it if exposure is suspected.

Risk: Extraction errors could affect financial analysis if accepted without review.

Mitigation: Check per-field needs_review flags and reconcile opening balance plus transactions against the stated closing balance before relying on the output.

## Reference(s):

- [DeepRead homepage](https://www.deepread.tech)
- [DeepRead dashboard](https://www.deepread.tech/dashboard)
- [DeepRead API endpoint](https://api.deepread.tech)
- [DeepRead service issues](https://github.com/deepread-tech/deep-read-service/issues)
- [ClawHub skill page](https://clawhub.ai/uday390/skills/deepread-bank-statements)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides the agent to submit bank statement files to DeepRead, poll for results, inspect confidence flags, and reconcile extracted balances.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
