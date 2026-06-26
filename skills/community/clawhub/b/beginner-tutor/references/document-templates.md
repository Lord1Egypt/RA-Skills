# Document Templates by Audience Type

Use these templates as starting points when generating the tutorial document.
Select based on the intended reader's background, then adapt to the subject.

---

## Template A: Technical/Engineering Audience

Best for: Readers with CS, engineering, math, or data science backgrounds.
Tone: Precise, structured, no hand-holding on technical concepts.
Style: Concept → structure → formula → code-like example → edge cases.

```markdown
# [Subject]: A Technical Primer

## Who This Is For
This guide assumes familiarity with [prerequisite technical concepts].
No prior knowledge of [subject] is required.

## Why [Subject] Exists
[Subject] solves the problem of [core problem].
In [reader's domain], the equivalent challenge is [bridge to their domain].

## Core Concepts

### [Concept 1]
**What it is**: [One-sentence definition]

**The structure**:
[Diagram, pseudocode, or data model showing the concept's structure]

**Formal definition**:
[Formula or precise definition]

**Example**:
[Worked numeric or code example with real values]

**Edge cases / common mistakes**:
- [Mistake 1]: [Why it happens and how to avoid it]
- [Mistake 2]: ...

### [Concept 2]
...

## How the Concepts Connect
[Dependency diagram or written explanation of the full mental model]

## Quick Reference

| Term | Definition | Formula / Notes |
|---|---|---|
| [Term 1] | [Definition] | [Formula if applicable] |
| ...

## Next Steps
[Specific, actionable next steps: tools to explore, topics to study next,
hands-on exercises to try]
```

---

## Template B: General / Non-Technical Audience

Best for: Readers with no technical background, from any walk of life.
Tone: Warm, approachable, curiosity-driven. No jargon without explanation.
Style: Story → concept → analogy → example → implication.

```markdown
# 零基础学懂 [Subject] / Understanding [Subject] from Scratch

## 这份教程适合谁 / Who This Is For
你不需要任何 [subject] 的基础。只要你对 [subject] 感到好奇，或者
工作中需要了解这个领域，这份教程就是为你写的。

You don't need any background in [subject]. If you're curious about it,
or need to understand it for work, this guide is for you.

## [Subject] 是什么，为什么重要 / What Is [Subject] and Why Does It Matter
[Subject] 解决的核心问题是 ___。

想象这样一个场景：[vivid, everyday scenario that illustrates the core problem].
[Subject] 就是用来解决这类问题的系统方法。

## 核心概念 / Core Concepts

### [Concept 1]: [Plain-language name]
**先说直觉** / The intuition first:

想象一下 [relatable everyday analogy]. [Subject] 中的 [concept] 就是同样的道理——
[explanation connecting analogy to concept].

**具体是什么** / What it actually is:

[Non-jargon explanation of the concept]

**一个例子** / A concrete example:

[Specific, worked example with real numbers or a mini-story]

**常见误解** / Common misconception:

很多人以为 [misconception]. 实际上 [correction], 因为 [reason].

### [Concept 2]
...

## 把所有概念串起来 / Putting It All Together
[Visual or narrative description of how all concepts connect]

## 你现在理解了什么 / What You Now Understand
读完这份教程，你应该能够：
- [Outcome 1]
- [Outcome 2]
- [Outcome 3]

## 关键词速查 / Key Terms
| 词汇 / Term | 解释 / Meaning |
|---|---|
| [Term] | [Plain-language definition] |
| ...

## 如果你想继续学 / If You Want to Go Deeper
[Approachable next steps: specific books, courses, tools, or communities]
```

---

## Template C: Practitioner / Adjacent Domain Audience

Best for: Experienced professionals learning an adjacent field.
Tone: Peer-to-peer, respects existing expertise, emphasizes the bridge.
Style: Bridge from known → new concept → practical application → differences from their domain.

```markdown
# [Subject] for [Their Profession]: What You Already Know Applies

## For the Experienced [Their Profession] Reader
This guide assumes deep familiarity with [their domain].
It's specifically designed to bridge from what you already know
to the new concepts in [subject].

## The Core Parallel
In [their domain], you deal with [analogous challenge].
[Subject] deals with exactly the same challenge, applied to [new context].
Most of the structure will feel familiar.

## What Maps Directly
| [Their Domain] | [New Subject] | Notes |
|---|---|---|
| [Familiar concept 1] | [New concept 1] | [Differences if any] |
| [Familiar concept 2] | [New concept 2] | ... |

## What's Genuinely New
These concepts don't have direct equivalents in [their domain]:
- **[New concept]**: [Explanation using their domain as a springboard]

## Practical Application
[Subject]-specific workflow applied to problems a [their profession] would recognize.

## Key Differences to Watch Out For
[Subject] differs from [their domain] in these important ways:
- [Difference 1]
- [Difference 2]

## Quick Reference
[Focused glossary of new terms only — skip things they already know]
```

---

## Choosing the Right Template

| Intended Reader | Template |
|---|---|
| Developer, data scientist, engineer | A: Technical |
| General public, student, non-technical professional | B: General |
| Doctor learning data science, lawyer learning finance, etc. | C: Adjacent Domain |
| Mixed audience | B as base, add technical details in callout boxes |

## Customization Notes

- Always replace "[Subject]" with the actual subject throughout
- For Chinese-speaking audiences, use Template B's bilingual approach or write fully in Chinese
- For short topics (< 5 concepts), collapse chapters; don't force structure onto thin content
- Always keep the Quick Reference / Key Terms section — it's the most-referenced part
