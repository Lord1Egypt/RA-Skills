---
name: eli5-tldr
description: Forces offering ELI5 or TLDR options after complex responses. Always present simplified alternatives.
tags: [communication, simplification, accessibility]
---

# ELI5 / TLDR Skill

**Rule: After any complex explanation, always offer ELI5 or TLDR.**

## When to Offer

Offer ELI5/TLDR when:
- Response exceeds 200 tokens
- Technical concepts involved
- Multiple steps or processes explained
- User might want quick summary

## Format

Add at end of response:

```
---
**Options:**
• [ELI5] — Explain like I'm 5
• [TLDR] — Too long, didn't read  
• [Full] — Keep current explanation
```

## ELI5 Style

- Simple analogies
- No jargon
- Concrete examples
- "Imagine..." / "Think of it like..."

## TLDR Style

- One sentence summary
- Key point only
- Bullet if multiple items

## Example

**Complex:**
> Token efficiency is achieved by reducing process narration, eliminating filler words, and presenting only outcomes. This reduces context window usage and improves information density.

**ELI5:**
> Think of it like texting. Don't say "I'm going to the store, then I'll buy milk, then I'll come home." Just say "Getting milk." Short and clear.

**TLDR:**
> Use fewer words. Get to the point.

## Activation

Always active. No trigger needed.