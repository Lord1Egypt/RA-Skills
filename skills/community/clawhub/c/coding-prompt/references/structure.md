## 6. Structural Wisdom

Patterns about when to patch vs. rewrite, and how to think about architecture.
For related anti-patterns, see also `references/anti-patterns.md`.

### 6.1 Patch vs. Rewrite Decision

| Signal | Action |
|--------|--------|
| Modified 1-2 times, clear improvement each time | Continue iterating |
| Modified 3+ times, only marginal improvement | Stop. Consider rewrite. |
| Fixes introduce new complexity to adapt old design | Rewrite. New complexity is a dead end in old architecture. |
| Fundamental design assumption is wrong | Rewrite immediately. Don't hesitate. |

**Rule of thumb**: 2 patches max on the same problem. On the 3rd, redesign.

### 6.2 Local Optimization Trap

Repeatedly polishing details without satisfaction usually means the **architecture is wrong**.

**Diagnosis signals**: Same module revised 3+ times without resolution; each fix only "alleviates" but never "solves"; the approach grows increasingly complex.

**Response**: Stop patching. Re-analyze from usage scenario. The real problem is usually one level up from where you're looking.

### 6.3 Cascade Verification

After any modification, verify not just "the changed part works" but "the unchanged parts still work." AI may silently alter dependency chains or delete indirectly-referenced code.

**Rule**: After changes, additionally check:
1. All callers of modified modules still function
2. Deleted code/imports have no remaining references
3. Core flow end-to-end test passes

### 6.4 Thorough Cleanup

When a feature is fully removed with no backward compatibility needed, remove everything — half-cleanup is worse than no cleanup. Future maintainers can't tell what's "intentionally kept" vs. "forgotten."

**Search scope**: Function names, import statements, comments referencing old design, documentation examples, conditional branches in other methods.

### 6.5 Collision Testing for Mapping/Transform Logic

Any design involving naming rules, key generation, hashing, or serialization must include collision testing during design phase — not testing phase.

**Rule**: When designing any mapping/transformation rule, construct boundary cases:
- Special characters (dots, underscores, spaces, CJK characters)
- Semantically equivalent inputs (`a.b` vs `a_b`)
- Edge cases (empty values, very long input, deep nesting)

If collision risk is found, resolve it in the design. Don't wait for testing.
