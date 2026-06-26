# Cross-Project Wisdom

Total: **10**

## `CW-ACCOUNTING-001` — Use exact-precision integer types for monetary representation
**From**: finance-bp-073--ledger, finance-bp-129--beancount · **Applicable to**: accounting

Both the Numscript ledger and Beancount parser mandates using Decimal (beancount) or MonetaryInt based on big.Int (ledger) instead of floating-point. This pattern ensures no rounding errors accumulate in financial calculations, critical for audit compliance in global markets.

## `CW-ACCOUNTING-002` — Mandatory initialization sequence before execution
**From**: finance-bp-073--ledger · **Applicable to**: accounting

The Numscript VM requires a strict initialization sequence: ResolveResources() then ResolveBalances() must both be called before Execute(). Skipping any step causes panics. This teaches that VM/script execution requires careful state setup—always verify prerequisites before running financial logic.

## `CW-ACCOUNTING-003` — Dual idempotency key strategy
**From**: finance-bp-073--ledger · **Applicable to**: accounting

Using both IdempotencyKey and IdempotencyHash together ensures robust duplicate detection: IdempotencyKey prevents exact retries while IdempotencyHash catches retries with different input parameters that would otherwise incorrectly succeed. Single-key approaches leave gaps in financial transaction safety.

## `CW-ACCOUNTING-004` — Log-before-commit event sourcing pattern
**From**: finance-bp-073--ledger · **Applicable to**: accounting

In the transaction processing pipeline, the log must be inserted before committing the transaction to maintain event sourcing integrity. This ensures the audit trail can always reconstruct state and supports rollback scenarios, critical for regulatory compliance in global accounting.

## `CW-ACCOUNTING-005` — Read Committed isolation with FOR UPDATE locks
**From**: finance-bp-073--ledger · **Applicable to**: accounting

When implementing balance operations, use Read Committed isolation level combined with FOR UPDATE row locks. This prevents concurrent transactions from creating inconsistent balances (e.g., both succeeding when they should fail due to insufficient funds), ensuring data integrity under concurrent load.

## `CW-ACCOUNTING-006` — Transitive closure for equivalence relationships
**From**: finance-bp-078--fava_investor · **Applicable to**: accounting

When building commodity groups or substantially identical fund relationships, apply transitive closure to infer complete equivalence. If A equals B and B equals C, then A, B, and C form one group. This ensures wash sale detection and TLH calculations are complete and accurate across all declared relationships.

## `CW-ACCOUNTING-007` — Canonical representative selection for relationship groups
**From**: finance-bp-078--fava_investor · **Applicable to**: accounting

When selecting a representative for a substantially identical fund group, always return the same representative ticker for any member of that group. Inconsistent representative selection causes non-deterministic calculations where the same ticker gets different partners depending on which group member is queried.

## `CW-ACCOUNTING-008` — Immutable monetary objects with __slots__
**From**: finance-bp-129--beancount · **Applicable to**: accounting

Constructing Amount or Position objects using immutable Decimal values with __slots__ = () pattern prevents accidental mutation of monetary values after creation. This immutability ensures financial calculations remain consistent throughout transaction processing and audit trails.

## `CW-ACCOUNTING-009` — Eliminate all MISSING values before presenting parsed data as complete
**From**: finance-bp-129--beancount · **Applicable to**: accounting

Parsed entries with MISSING sentinel values are incomplete and cannot be used for financial reporting. All MISSING values must be resolved through booking and interpolation before claiming parsed entries are ready for balance calculations or realized/unrealized gains computation.

## `CW-ACCOUNTING-010` — Strict schema compatibility across class hierarchies
**From**: finance-bp-078--fava_investor, finance-bp-129--beancount · **Applicable to**: accounting

When extending base classes with additional functionality (like ScaledNAV extending RelateTickers), maintain compatibility with existing metadata schemas. Schema divergence causes extended classes to miss relationships declared for the base class, breaking wash sale detection and TLH recommendations.
