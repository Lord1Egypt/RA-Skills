---
name: bank-recon
description: Perform bank reconciliation between bank statements and general ledger files. Supports bank statement PDF ingestion, conversion of PDF statements into structured Excel data, custom amount thresholds, ID/key matching, and semantic description matching. Use when the user wants to read a bank statement PDF or Excel file, convert statement activity into a workbook, reconcile bank activity to GL transactions, identify matched and unmatched items, and generate an Excel workbook with reconciliation results, a summary tab, and separate unreconciled-bank and unreconciled-GL tabs.
---

# Bank Reconciliation Skill

Reconcile bank statement rows against GL rows and produce an `.xlsx` workbook that is immediately reviewable by an accountant.

## Workflow

1. Identify the bank statement path and GL workbook path.
2. Accept either a bank statement `.xlsx` file or a bank statement `.pdf` file.
3. If the bank statement is a PDF, run the workflow so it first extracts the bank statement lines into a structured workbook, then reconciles that extracted workbook to the GL.
4. Confirm the reconciliation threshold. Default to `0.00` unless the user asks for a tolerance.
5. Run `scripts/recon_logic.py` with the bank file, GL file, output file, and threshold.
6. Return the generated workbook and summarize:
   - matched bank row count
   - matched GL row count
   - unreconciled bank row count
   - unreconciled GL row count
5. If the user asks for follow-up analysis, use the `Summary`, `Unreconciled Bank`, and `Unreconciled GL` tabs first.

## Output Workbook

The generated workbook should contain these tabs:

- `Summary`: threshold, matched counts, unreconciled counts, and basic totals
- `Recon Results`: matched groupings with match basis and variance notes
- `Unreconciled Bank`: bank rows not matched to the GL
- `Unreconciled GL`: GL rows not matched to the bank

## Command

```bash
python3 scripts/recon_logic.py <bank_xlsx_or_pdf> <gl_xlsx> <output_xlsx> [threshold]
```

When the bank input is a PDF, the script also creates a companion extracted workbook beside the PDF (same basename with `_extracted.xlsx`) before running reconciliation.

## Matching Logic

Use a layered approach:

1. Preserve the original signs from both source files in the output.
2. Compare bank and GL amounts using absolute values for matching so bank polarity and accounting debit/credit polarity can reconcile without rewriting displayed source amounts.
3. Match by shared extracted keys such as batch IDs, invoice IDs, vendor IDs, customer IDs, and tax/payment references.
4. Allow one-to-one, one-to-many, many-to-one, and grouped many-to-many matches when totals fall within threshold.
5. For remaining items, use semantic name grouping plus summed-amount comparison.
6. Preserve unmatched rows in dedicated tabs instead of dropping them from the deliverable.

## Notes

- Read the first worksheet from each input workbook.
- Expect simple three-column inputs: date, amount, description/memo.
- For text-based bank statement PDFs, the script extracts transaction rows by reading the PDF content streams and reconstructing the transaction table into a workbook.
- The PDF path is best for digital statements with selectable text; scanned-image PDFs would still need OCR or a multimodal extraction path.
- Keep the workbook generation dependency-light so it can run in minimal Python environments.
