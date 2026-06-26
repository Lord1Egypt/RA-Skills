# Matching rules

## Reason codes

- `R001`: exact model + exact variant match
- `R002`: model exact, one soft-field inferred
- `R003`: likely match, manual review required
- `R101`: storage/RAM mismatch
- `R102`: bundle vs standalone mismatch
- `R103`: condition mismatch
- `R104`: brand/model conflict

## Rule order

1. Hard identifier check
2. Variant parity check
3. Condition parity check
4. Soft similarity fallback
5. Confidence scoring and decision

