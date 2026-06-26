## Description: <br>
Processes raw accounting source documents, including PDFs, CSVs, bank statements, invoices, receipts, 1099s, and payroll reports, into standardized transaction records for QuickBooks Online import. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Accounting operators and agents use this skill to batch-ingest client documents during month-end close, classify transactions, detect duplicates, flag exceptions, and prepare files for QuickBooks Online import. It is not intended for bank reconciliation, P&L variance analysis, single manual journal entries, or AR collections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live QuickBooks Online chart-of-accounts lookup may expose sensitive accounting metadata or use the wrong client account if credentials or consent are not confirmed. <br>
Mitigation: Use --no-qbo-coa for offline processing until the correct QuickBooks account, credentials, and client consent are confirmed. <br>
Risk: Generated import CSVs can introduce incorrect accounting records if duplicates, low-confidence categories, or extraction exceptions are imported without review. <br>
Mitigation: Review the exceptions tab, duplicate flags, confidence scores, and import CSV before importing anything into QuickBooks Online. <br>
Risk: PDF and image extraction can fail or require OCR tooling, which may leave receipt or scanned-document data incomplete. <br>
Mitigation: Install the documented optional extraction tools where appropriate and manually review records flagged for failed PDF extraction or missing image OCR. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/document-ingestion) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands, plus generated Excel workbook and CSV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces DocIngestion_{slug}_{YYYYMMDD}.xlsx and DocIngestion_{slug}_{YYYYMMDD}_QBO_Import.csv; exceptions and low-confidence categorization require review before QBO import.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
