# Structuring notes

Use raw OCR first, then decide whether to organize the content.

Suggested post-processing patterns:
- plain text screenshots → keep paragraph order
- chat screenshots → preserve message order and speaker labels when visible
- table screenshots → group by rows/columns carefully, avoid inventing headers
- statement/ledger screenshots → split into repeated fields such as date/time/currency/merchant/amount

Recommended workflow:
1. Run `raw` mode and review the OCR text.
2. If the image has obvious repeated row patterns, run a structuring mode.
3. Present both the cleaned result and the raw fragments when users need verification.
4. Only after user confirmation, use the result in tables, summaries, or documents.

Core rule:
- if confidence is low or grouping is ambiguous, show the raw OCR text and mark uncertain parts as `待确认`
- do not invent names, categories, invoice status, or business meaning that the image does not clearly support

Current built-in structuring:
- `transactions`: optimized for bank/card/statement-like screenshots where OCR returns one field per line

Known limitations:
- not all screenshot layouts can be perfectly structured by fixed heuristics
- payment-channel prefixes and broken merchant names may still need human review
- raw OCR is the source of truth when structured output conflicts with visible image content
