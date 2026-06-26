# Session Claim Ledger Template

Use this reference when the user wants to carry reasoning context across turns
by pasting prior notes into the conversation. This package does not include any
helper program or automatic state mechanism.

## Import rules

Treat any prior ledger, pasted notes, connector result, or previous answer as
candidate context only. Imported material enters the current session as
`[CLAIM]`, not `[TRUTH]`, even when it was previously marked verified.

Ask the user to paste or provide the relevant context if prior claims are
needed. Do not assume prior notes remain valid without re-checking them in the
current context.

## Lanes

| Lane | Use for | Promotion rule |
|---|---|---|
| `[TRUTH]` | Verified in this session by math, code result, source, measurement, or explicit stipulation | Must pass the Ground-Truth Test |
| `[CLAIM]` | User-provided, source-provided, or imported prior statements | Can promote only after re-verification |
| `[ASSUMPTION]` | Unverified belief or convention used as if true | Must be tested, bounded, or marked fragile |
| `[CONSTRAINT]` | Hard limit with source, threshold, and consequence | Must identify cost of violation |
| `[UNKNOWN]` | Missing fact that could affect the answer | Must include resolution plan and sensitivity |

## Carry-forward summary block

At the end of a substantial answer, include this block only when there are
reusable claims worth preserving. It is a text proposal for human review.

```markdown
### Carry-Forward Ledger Summary (copy/paste only)
+ [TRUTH]      <statement>   evidence=<...>   scope=<...>
+ [CONSTRAINT] <statement>   source=<...>     threshold=<...>
+ [UNKNOWN]    <question>    why_it_matters=<...> fastest_test=<...>
```

Do not include secrets, credentials, private customer data, unreleased internal
plans, regulated data, or confidential business facts in this block.
