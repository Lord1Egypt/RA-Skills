# Design Notes

> **[中文版](./DESIGN.zh-CN.md)**

## Problem: Sycophancy is Structural, Not Attitudinal

The core insight from [ArXiv 2602.23971](https://arxiv.org/abs/2602.23971) is that LLM sycophancy is a **structural side effect of RLHF alignment**, not a personality trait. Models are trained to be helpful — and helpfulness, in the RLHF sense, correlates with user satisfaction — which correlates with validation.

The usual fix — adding instructions like *"please be objective"* — doesn't work because the model has already learned that agreeable responses get rewarded. You can't instruct your way out of a training-reward correlation.

---

## Solution: Remove the Space for Agreeableness

The paper's key finding: **changing the structure of the prompt changes the sycophancy rate more than any explicit instruction**.

Three examples that work:
1. Ending with a question mark instead of a period → lowest sycophancy
2. Embedding the assumption in a question (*"Is X correct?"*) vs. a statement (*"X is correct, right?"*) → question wins
3. Inviting counterarguments explicitly → model defaults to challenge mode instead of validation mode

The fix isn't "tell the model to be critical." The fix is **structurally removing the path of least resistance for agreeableness**.

---

## Three-Layer Architecture

### Layer 1 — Automatic Prompt Transformation (Hook)

A `UserPromptSubmit` hook runs on every prompt before it reaches the model. It scans for confirmatory phrasing and rewrites it:

```
"这样做对吧？" → "这样做有什么问题？"
```

This is the **automatic, zero-friction layer**. No user action needed, no activation required. The transformation happens before the model ever sees the sycophancy-inducing phrasing.

**Why this is a hook, not a prompt instruction:**
- Hooks run at the harness level, before the model
- Prompt instructions get filtered through the model's own tendency to agree
- Hook transformation is deterministic — the same input always gets the same rewrite

**Limitation:** Shell-based hooks are Claude Code-specific. OpenClaw would require a Plugin SDK hook.

### Layer 2 — Critical Response Mode (SKILL)

When the user explicitly activates the skill (via keyword or semantic trigger), the model enters a heightened critical mode with:

1. **Presupposition Challenge First** — any embedded assumption is interrogated before the question is answered
2. **No Direct Confirmation** — even correct assumptions get a harder examination before validation
3. **Active Counterexamples** — every positive evaluation is preceded by a substantive objection
4. **Confirmatory Pattern Detection** — after 3+ consecutive confirmatory prompts, the model self-interrupts with a challenge

This layer addresses the **response side** of sycophancy — what the model says when Layer 1 can't intercept (e.g., prompts from other channels, non-shell interfaces).

### Layer 3 — Persistent Rules (CLAUDE.md / SOUL.md)

The most durable layer. Rules are installed into the agent's persistent instruction files, so they survive across sessions and don't require re-activation.

This layer addresses the **baseline behavior** — ensuring the agent starts in critical mode by default, not just when explicitly reminded.

---

## Why Three Layers?

| Attack Vector | Layer That Blocks It |
|-------------|---------------------|
| Confirmatory prompt via shell | Layer 1 (hook) |
| Confirmatory prompt via API / other channel | Layer 2 (skill activation) |
| Model defaulting to agreeable baseline | Layer 3 (persistent rules) |
| User saying "对吧？" | Layer 1 transforms → "有什么问题？" |
| User saying "没问题吧" without explicit trigger | Layer 2 activates on semantic pattern |
| Model starting a new session without reminders | Layer 3 loads from CLAUDE.md |

No single layer covers all attack vectors. Layer 1 is automatic but limited to one interface. Layer 2 is powerful but requires activation. Layer 3 is persistent but passive. Together they close the gap.

---

## Optimization History

This skill was **automatically optimized via 40 rounds of mutation testing** using [cjl-autoresearch-cc](https://github.com/0xcjl/cjl-autoresearch-cc), scoring 10/10 across 10 quality dimensions:

- Description clarity
- Trigger coverage (Chinese + English)
- Command completeness
- Error handling (idempotency, file-not-found, platform detection)
- Install/uninstall symmetry
- Cross-platform consistency
- Status reporting accuracy
- Reference quality

Key improvements made during optimization:
- Add idempotency checks to all install/uninstall steps
- Handle `UserPromptSubmit` array missing from settings.json
- Handle `CLAUDE.md` and `SOUL.md` missing from filesystem
- Bilingual trigger keywords (Chinese + English semantic triggers)
- Layer 1/2/3 cross-references for clarity

---

## Limitations

- **Layer 1** only works in Claude Code (shell hook interface not available in OpenClaw)
- Layer 1 transforms at the **textual** level — it can't understand semantics, only pattern-matches phrasing
- The skill's effectiveness depends on the underlying model still being aligned with critical thinking — if the base model is too agreeable, all three layers fight the same current
