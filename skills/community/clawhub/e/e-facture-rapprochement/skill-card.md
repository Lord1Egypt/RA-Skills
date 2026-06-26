## Description: <br>
Ingests invoices, receipts, and bank statements, then reconciles payments to invoices and writes Pocket-Claw accounting JSON outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trendex](https://clawhub.ai/user/trendex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Accounting teams and finance operators use this skill to process client invoice folders, extract unresolved receipt or PDF data, reconcile bank transactions, and review unpaid invoices, orphan payments, excluded lines, and records requiring human validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes sensitive invoices, receipts, and bank statements. <br>
Mitigation: Run it only on intended accounting folders, start in the default sandbox, and use --real only after reviewing the output. <br>
Risk: Low-confidence or high-value LLM extractions can affect reconciliation accuracy. <br>
Mitigation: Verify documents flagged for human review before relying on generated reconciliation files. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/trendex/e-facture-rapprochement) <br>
- [Invoice extraction reference](references/invoice-extraction.md) <br>
- [Bank formats reference](references/bank-formats.md) <br>
- [Matching rules reference](references/matching-rules.md) <br>
- [Output contract reference](references/output-contract.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes company.json and rapprochement.json through scripts/main.py; sidecar JSON may be required for unstructured documents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
