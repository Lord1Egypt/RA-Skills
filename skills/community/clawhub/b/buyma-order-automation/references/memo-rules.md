# Memo Rules

## Goal

Ensure every processed BUYMA order has a valid 6-digit order number in receipt memo.

## Rules

### Case 1: memo already contains a valid 6-digit order number
- Do not rewrite
- Treat as already numbered

### Case 2: memo contains text only
- Prepend the new 6-digit order number
- Preserve existing text after it

Example:
existing memo: VIP
new order no: 123457
result: 123457 VIP

### Case 3: memo contains a numeric value shorter than 6 digits
- Prepend the new 6-digit order number
- Preserve existing value after it

Example:
existing memo: 345
new order no: 123457
result: 123457 345

### Case 4: memo empty
- Write only the 6-digit order number

## Scope

Apply these rules in:
- regular daily run
- ad hoc range run
