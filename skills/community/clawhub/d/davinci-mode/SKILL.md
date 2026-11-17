---
name: davinci-mode
description: Explore a design or strategy decision through distinct straightforward, hybrid and creative approaches, with concrete tradeoffs and a reasoned recommendation. Use when the user wants options before choosing, not after they have already decided.
---

# Davinci Mode

Give the user a real design space, not a single recommendation dressed up as a choice.

## Explore three useful lanes

- **Straightforward:** the conventional path. Explain which existing components it uses, implementation effort and known limits.
- **Hybrid:** a practical combination that changes a meaningful tradeoff, not just the wording.
- **Creative:** a non-obvious mechanism with a plausible path to implementation. Identify its riskiest assumption and the cheapest way to test it.

Each option should be viable under the user's actual constraints. Do not invent an obviously inferior option to make your favourite win. If constraints eliminate a lane, explain why rather than manufacturing filler. Add a no-change option when it is genuinely competitive.

For each option state what changes, what it buys, what it costs, what could fail and when to choose it. Distinguish facts from estimates. Inspect relevant existing systems before proposing architectural changes; verify time-sensitive product or pricing assumptions with current primary sources.

## Recommend without erasing the choice

Recommend one option against the user's stated priorities. Say which uncertainty could change that recommendation. Keep competing options strong enough that the user can reasonably select them.

Use a compact comparison or separate labelled paragraphs. Use the host's question UI when available and useful; otherwise ordinary prose is sufficient. A sketch helps only when it makes a meaningful difference visible.

## Stop exploring when a choice is made

This skill structures a decision; it does not authorise implementation, spending, publication or external actions. If the user already chose a direction, help execute that direction instead of reopening the design space. Answer factual questions directly. Do not impose three options on a simple confirmation.
