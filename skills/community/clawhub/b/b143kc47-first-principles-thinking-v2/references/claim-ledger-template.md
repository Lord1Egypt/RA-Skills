# Claim Ledger Template

Use this reference when the user wants to carry durable reasoning context across
turns without enabling any local helper or filesystem persistence.

## Import rules

Treat any prior ledger, pasted notes, connector result, or previous answer as
candidate context only. Imported material enters the current session as
`[CLAIM]`, not `[TRUTH]`, even when it was previously marked verified.

Never read or write local files on behalf of this reference. Ask the user to
paste or provide the relevant context if prior claims are needed.

## Lanes

| Lane | Use for | Promotion rule |
|---|---|---|
| `[TRUTH]` | Verified in this session by math, code result, source, measurement, or explicit stipulation | Must pass the Ground-Truth Test |
| `[CLAIM]` | User-provided, source-provided, or imported prior statements | Can promote only after re-verification |
| `[ASSUMPTION]` | Unverified belief or convention used as if true | Must be tested, bounded, or marked fragile |
| `[CONSTRAINT]` | Hard limit with source, threshold, and consequence | Must identify cost of violation |
| `[UNKNOWN]` | Missing fact that could affect the answer | Must include resolution plan and sensitivity |

## Export block

At the end of a substantial answer, include this block only when there are
reusable claims worth preserving. It is a proposal for the user to copy, not an
automated write operation.

```markdown
### Claim Ledger Export (copy/paste only)
+ [TRUTH]      <statement>   evidence=<...>   scope=<...>
+ [CONSTRAINT] <statement>   source=<...>     threshold=<...>
+ [UNKNOWN]    <question>    why_it_matters=<...> fastest_test=<...>
```

Do not include secrets, credentials, private customer data, unreleased internal
plans, regulated data, or confidential business facts in this export block.
