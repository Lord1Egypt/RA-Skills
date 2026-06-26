# Output Format Specification

## Per-Issue Format

Every issue found must be reported with:

```
### 🔴/🟡/🟢 [Severity]: [Issue Title]

**结论**: Confirmed / Mitigated / False Alarm / Disputed
[If Critical + Four-Eyes verified: 👁️ Four-Eyes Verified by [subagent-name]]

**源码证据**: [file:line range — the specific code that proves the issue]
[Optional: quote the relevant code block]

**风险场景**: [Concrete scenario — user does X → system does Y → consequence Z]

**修复建议**: [Actionable, specific fix — not "consider improving"]
```

## Synthesis Format (after all subagent reports)

Aggregate findings into:

### 1. Summary Table by Severity

```
| # | 问题 | 来源(审计维度) | 根因(一行) | 👁️ |
|---|------|--------------|----------|-----|
```
`👁️` column: ✅ if Four-Eyes verified, blank otherwise.

### 2. Priority Matrix

```
| 优先级 | 问题 | 工作量 | 影响范围 |
|--------|------|--------|----------|
| P0 🔴 | ... | 1行代码 | 所有用户 |
| P1 🔴 | ... | ~30行 | 特定场景 |
```

### 3. Simplicity Score (NEW v1.1.0)

A 1-5 rating of how well the codebase's complexity matches its problem domain:
- **5/5** 🏆 — Elegantly minimal. Every line earns its place.
- **4/5** ✅ — Clean. Minor nitpicks.
- **3/5** ⚠️ — Acceptable. Some bloat but functional.
- **2/5** ❌ — Over-engineered. Needs refactoring.
- **1/5** 🚨 — Massively bloated. Do not merge.

### 4. Executive Summary

One paragraph that captures the overall quality assessment + top 3 action items.

## Emoji Convention

- 🔴 Critical — System violates core guarantees
- 🔴 High — Significant impact, fix before next release
- 🟡 Medium — Degrades UX or creates operational risk
- 🟢 Low — Cosmetic, theoretical, or well-mitigated
- ✅ Mitigated — Concern exists but defended elsewhere
- ❌ False Alarm — Concern does not exist
- ⚠️ Disputed — Four-Eyes reviewers disagree (needs human)
- 👁️ Four-Eyes Verified — Independently confirmed by a second subagent

Use the emoji in the severity tag, not the conclusion tag.
