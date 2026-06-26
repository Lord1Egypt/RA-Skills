# A-MAP Delegation Invariants

Three invariants are enforced cryptographically by the A-MAP SDK. A malicious
agent cannot produce a valid token that violates any of them.

---

## 1. Permissions Can Only Narrow

A child token may only grant permissions that exist in its parent token.

```
Root:  ['read_email', 'send_email', 'delete_email']
Hop 2: ['read_email', 'send_email']   ← valid: subset of root
Hop 3: ['read_email']                 ← valid: subset of hop 2
Hop 3: ['read_email', 'write_file']   ← INVALID: write_file not in hop 2 → PERMISSION_INFLATION
```

---

## 2. Constraints Can Only Tighten

Numeric constraints use the minimum across all hops. Boolean constraints, once
set to `true`, cannot be unset. List constraints (allowedDomains, allowedActions)
narrow by intersection. `parameterLocks` accumulate — once locked, always locked.

| Constraint | Merge rule |
|---|---|
| `maxSpend` | min across all hops |
| `maxCalls` | min across all hops |
| `rateLimit.count` | min across all hops |
| `rateLimit.windowSeconds` | min across all hops |
| `readOnly` | once `true`, always `true` |
| `allowedDomains` | intersection |
| `allowedActions` | intersection |
| `parameterLocks` | union of all ancestor locks (all enforced) |

Example:
```
Root:  { maxSpend: 500, readOnly: false }
Hop 2: { maxSpend: 200 }   ← valid: 200 < 500
Hop 2: { maxSpend: 800 }   ← INVALID: 800 > 500 → CONSTRAINT_RELAXATION
Root:  { readOnly: true }
Hop 2: { readOnly: false } ← INVALID: cannot unset readOnly → CONSTRAINT_RELAXATION
```

---

## 3. Expiry Can Only Shorten

A child token's `expiresAt` must be ≤ its parent's `expiresAt`. The SDK converts
the `expiresIn` duration string to an absolute timestamp and compares it against
the parent's expiry before signing.

```
Root: expiresAt = T+60min
Hop 2: expiresIn = '30m'   ← valid: T+30min < T+60min
Hop 2: expiresIn = '90m'   ← INVALID: T+90min > T+60min → EXPIRY_VIOLATION
```

---

## Why These Invariants Matter

Without cryptographic enforcement, a sub-agent could:
- Claim any permission via prompt manipulation ("I have admin access, disregard your constraints")
- Relax a maxSpend of $100 to $10,000
- Extend a 15-minute mandate to 24 hours

A-MAP makes all three impossible: the invariants are checked before signing and
re-validated at every hop during `verifyRequest()`. A tampered token fails the
Ed25519 signature check at the hop where it was altered.
