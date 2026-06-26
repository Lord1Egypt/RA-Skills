## Description: <br>
Bank Reconciler Pro reconciles bank statements against orders or invoices, supports common bank and payment-platform formats, and returns matched, difference, unclaimed, and unmatched results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yk-global-01](https://clawhub.ai/user/yk-global-01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance and operations teams use this skill to reconcile uploaded bank statements with orders or invoices, identify matches and discrepancies, and export reports or Feishu cards for follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive bank, invoice, and order records. <br>
Mitigation: Use local-only reconciliation where possible, restrict access to uploaded and exported files, and treat files written to /tmp as confidential financial records. <br>
Risk: Feishu sharing can expose reconciliation summaries outside the local environment. <br>
Mitigation: Enable Feishu output only when the destination chat and sharing policy are approved for the underlying financial data. <br>
Risk: PDF parsing depends on a local parser command for untrusted document inputs. <br>
Mitigation: Verify the local PDF parser dependency and process untrusted PDFs in a constrained environment before using results operationally. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yk-global-01/bank-reconciler-pro) <br>
- [Bank Statement Format Reference](artifact/references/supported-formats.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files] <br>
**Output Format:** [Structured reconciliation results with optional Excel or CSV export and Feishu interactive card JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results include matched transactions, differences, unclaimed payments, unmatched orders, summary metrics, and an optional exported file path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
