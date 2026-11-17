---
name: openclaw-finance-voucher
description: Generate import-ready Chinese finance workbooks from monthly input VAT invoice exports or bank statement exports. Use when OpenClaw or Codex must turn Excel invoice exports containing sheets such as 信息汇总表, 发票基础信息, 进项税, 进项税（有数量的）, 凭证/凭证转出, and 科目编码, or bank detail exports containing 账户明细, into complete financial workbooks with source tables, voucher rows, account-code mapping, bank-fee aggregation, special-ticket handling, and audit notes.
---

# OpenClaw Finance Voucher

## Overview

Use this skill to produce finance-ready Excel workbooks from monthly Chinese invoice exports or bank statement exports. The output must be suitable for accounting review and financial-system import, not just a formatted report.

For detailed invoice rules, mapping logic, special cases, and checks, read [workflow.md](references/workflow.md) before implementing the workbook.
For bank-statement details, read [bank_statement.md](references/bank_statement.md) when the source is an `账户明细` workbook or the user asks for monthly bank流水 / 手工对账表.

## Execution Contract

1. Treat the invoice export as the source of truth.
2. Preserve source sheets when the user provides them, especially `信息汇总表` and `发票基础信息`.
3. Generate the requested output sheets:
   - `信息汇总表`
   - `发票基础信息`
   - `进项税`
   - `进项税 (有数量的)`
   - monthly voucher export sheet, usually named like `202607`
   - `科目编码`
   - optional audit sheets such as `处理逻辑说明` and `科目映射清单`
4. Reuse existing chart-of-accounts and historical voucher patterns. Do not invent account codes.
5. Handle special tickets explicitly: electricity, freight/agent freight, red invoices, foreign-currency settlement, one invoice with multiple line items, and one invoice split across multiple material accounts.
6. For bank statements, preserve the manual-template row order and aggregate visible `费用外收` rows by transaction date into one line using the last visible fee row's balance and the day count. Do not infer missing fee rows by default; surface balance or total mismatches for finance review unless the user explicitly authorizes a manual补回.
7. Keep the workbook import-ready: stable columns, typed numbers, voucher rows balanced, and no broken formulas.
8. Do not commit changes unless the user explicitly asks.

## Required Alignment

Before generating the workbook, confirm or infer these points:

- Month boundary: normally use invoice issue date (`开票日期`) inside the target month.
- Filing month: normally set `进项税` `所属月份` to the following month.
- Voucher numbering: continue from the previous month or user-specified starting number.
- Personnel fields: preserve the prior template's `制单人`, `审核人`, and `记账人`.
- Account mapping: use the existing `科目编码` sheet and prior voucher history. If a supplier/item is new, map to the closest existing account and record it in `科目映射清单`.

Ask the user only when a decision changes accounting treatment or import compatibility.

## Workflow

1. Inspect the source workbook and the prior template or historical voucher workbook.
2. Build invoice-level and line-item-level datasets.
3. Derive account mapping by supplier, goods/service name, and prior vouchers.
4. Generate the `进项税` sheet at invoice level.
5. Generate the `进项税 (有数量的)` sheet at line-item level.
6. Generate voucher export rows grouped by invoice number.
7. Add `处理逻辑说明` and `科目映射清单` so a finance worker can audit assumptions.
8. Verify totals and render key sheets before final delivery.

## Verification

Before delivering:

- Reconcile source `金额`, `税额`, and `价税合计` totals to generated `进项税`.
- Reconcile voucher debit total to voucher credit total.
- Confirm each generated voucher group has the expected debit/material or expense line, input tax line, and credit/AP or bank line.
- Scan for formula errors.
- Render key sheets visually and fix clipped headers, unreadable columns, or malformed identifiers.
- State any assumptions that still require finance review.
