# Four-Eyes Cross-Verification Protocol

## Origin

Bavota & Russo (2015), "Four Eyes Are Better Than Two: On the Impact of Code Reviews on Software Quality", found that multiple independent reviewers examining the same code catch 60%+ more real defects than a single reviewer. This protocol operationalizes that finding for AI subagent review.

## Protocol

### When to activate

Four-Eyes cross-verification is **mandatory** for:
- Any finding classified as **Critical** by a primary subagent
- Any finding where the primary subagent reports "confirmed with medium confidence" or similar hedging

### How to execute

1. **Spawn a second subagent** with the **exact same issue prompt** as the primary
2. The second subagent must have a **different dimension focus** than the primary (to avoid groupthink)
3. The second subagent sees only the issue prompt — NOT the primary's findings (to ensure independence)
4. Both reports are compared after completion

### Resolution rules

| Primary says | Second says | Final conclusion |
|---|---|---|
| Critical | Critical | **Confirmed** + `👁️ Four-Eyes Verified` badge |
| Critical | High/Medium/Low | **Confirmed** at the higher severity. Add note: "Second reviewer rated lower at [severity]." |
| Critical | Mitigated | **Mitigated** (the second found a defense the first missed). Keep both reports in appendix. |
| Critical | False Alarm | **False Alarm** (the second found the issue doesn't exist). Keep both reports in appendix. |
| Critical | Disputed (disagrees but can't reclassify) | **Disputed** — flag for human reviewer. Include both conclusions. |

### Reporting format

In the final report, Critical findings carry:

```
### 🔴 Critical: [Issue Title]
👁️ Four-Eyes Verified by [subagent-2-name]
```

Disputed findings carry:

```
### ⚠️ Disputed: [Issue Title]
🔴 Subagent 1 ([dimension]): Critical — [summary]
🟢 Subagent 2 ([dimension]): Mitigated — [defense found]
→ Human review recommended.
```

## Cost/benefit guidance

- **Small codebase (<20 files)**: Four-Eyes only on findings the auditor is uncertain about
- **Medium codebase (20-100 files)**: Four-Eyes on all Critical findings
- **Large/mission-critical codebase**: Four-Eyes on Critical + High findings

The additional cost is ~25-40% more subagent compute, but the false-positive reduction makes it worthwhile for release-blocking decisions.
