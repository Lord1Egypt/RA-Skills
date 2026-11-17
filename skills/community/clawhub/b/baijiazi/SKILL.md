---
name: baijiazi
description: >-
  Use only when the user explicitly invokes baijiazi or 败家子 and includes the
  exact confirmation token CONFIRM_BURN. Burns a confirmed token budget with
  bounded, read-only expansion; never use for unconfirmed, concise, high-stakes,
  or project-editing tasks.
license: MIT
metadata:
  version: "0.1.0"
  owner: VincentJiang06
  keywords: [败家子, 烧token, 展开, 低价值, 确认]
---

# baijiazi (败家子)

Purpose: spend an explicitly approved token budget quickly while still producing something organized, bounded, and somewhat useful.

## Hard Gate

STOP unless both are true:

1. The user explicitly names `baijiazi`, `败家子`, or says to use this skill.
2. The user includes the exact confirmation token `CONFIRM_BURN`.

If the user named the skill but did not include `CONFIRM_BURN`, ask for that one confirmation and stop. Do not produce the burn output yet.

## Boundaries

- MUST NOT modify user project files.
- MUST NOT run destructive commands, create commits, install packages, access secrets, browse the web, or use unrelated tools just to spend tokens.
- MUST NOT fabricate citations, quotes, links, dates, measurements, test results, source provenance, or tool results.
- MUST NOT use burn mode for medical, legal, financial, security, safety, or crisis topics. Give a concise careful answer instead.
- MUST stop after one confirmed burn pass. A later turn needs a fresh explicit invocation and `CONFIRM_BURN`.

## Burn Method

After confirmation, expand by adding useful structure rather than filler:

- State that this is an intentional confirmed token-burn output.
- List assumptions and boundaries.
- Build several lenses, examples, options, tradeoffs, and failure modes.
- Use bounded read-only subagents only when multi-agent tools are available and the confirmed budget is large enough.
- Merge and deduplicate any subagent findings; never paste raw subagent transcripts.

## Output Shape

Use this structure unless the user requested a specific format:

1. Intentional burn note.
2. Assumptions and scope.
3. Core framing.
4. Expanded analysis sections.
5. Risk and failure-mode pass.
6. Worked miniature or scenario.
7. Compact reusable core.

Make the answer long by adding lenses, concrete examples, and synthesis. Do not repeat filler.

