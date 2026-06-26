# ELI5 — Explain Like I'm 5

**Version:** 1.0.0  
**Author:** coghost

**Turn any complex topic into something a child could understand.**

---

## Why ELI5?

| Dimension | Regular Explanation | ELI5 |
|-----------|-------------------|------|
| Audience | Requires background knowledge | Zero门槛 |
| Understanding Speed | Slow, needs digestion | Fast, visual |
| Memory | Easy to forget | Analogies stick |
| Depth | May skip key points | Forces you to the core |

---

## The Biggest Benefit: Feynman Test

> "If you can't explain something in simple terms, you don't understand it."

ELI5 is fundamentally a **self-check tool** — the explainer is forced to truly understand in order to find a good analogy.

---

## When to Use ELI5

**Perfect for:**
- Testing your own understanding of a new domain
- Explaining concepts to non-experts
- Breaking mental models and discovering what you actually understand

**Not suitable for:**
- Situations requiring precise answers
- Technical discussions between professionals
- Real-time news judgment

---

## Limitations

| Issue | Description |
|-------|-------------|
| Oversimplification | May lose important details or boundary conditions |
| False understanding | Knowing the analogy ≠ understanding the concept |
| Not for precise content | Mathematical proofs, exact values can't ELI5 |
| Creativity-dependent | Without a good analogy, results are mediocre |
| Execution variance | Different people/models produce different quality |

---

## Quick Start

```
/eli5 schrödinger's cat   # explain any concept
/eli5 help                 # show all commands
/eli5 lang <lang>          # switch language (en/zh/es/kr/...)
/eli5 bonus on             # enable bonus explanations
/eli5 steps 5              # adjust max steps (default: 3, max: 5)
/eli5 fetch on             # enable auto-fetch from web
/eli5 <concept> --fetch   # fetch latest content for one answer
```

---

## The Rules

1. **Language priority:** env var > `/eli5 lang` > fallback English
2. **Be conversational, not formulaic** — sound like a smart friend explaining, not a textbook
3. **Assume nothing** — the user knows zero technical terms
4. **Bridge: unknown → known** — pick one familiar thing and stick with it
5. **Max n steps** — short sentences, one action each
6. **Concrete example** — one real thing the reader can picture
7. **Have personality** — vary your explanations. Humor and contrast beat dry lists
8. **Bonus** (default: off) — only show when genuinely needed
9. **Freshness indicator** — always shown after explanation
10. **Fresh fetch** — auto-fetch from web when enabled

---

## Examples

**Schrödinger's cat**
A cat that is both alive AND dead — until you open the box.
Try it: `/eli5 schrödinger's cat`

**The Chinese Room**
A person who pretends to understand Chinese but follows a rulebook instead.
Try it: `/eli5 chinese room`

**The Ship of Theseus**
If you replace every plank of a ship, is it still the same ship?
Try it: `/eli5 ship of theseus`

---

## Freshness Indicator

After every explanation, you'll see:

```
[Data: ~2024] [Freshness: ██████░░░░ 65%] [→ --fetch]
```

- **80-100% (Stable):** No action needed
- **50-79% (Evolving):** Consider using `--fetch`
- **0-49% (Outdated):** Strongly recommend `--fetch`

When `--fetch` succeeds, the actual latest date/version is shown instead of the estimate.
