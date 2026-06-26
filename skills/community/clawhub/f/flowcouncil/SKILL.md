---
name: flowcouncil
description: Your AI think tank. Five domain-expert Fellows debate any idea, decision, or creative work. Three rounds. One verdict that's actually useful.
version: 2.0.0
author: flo
---

# Flow Council

An AI think tank. Five domain-expert Fellows. Three rounds. One verdict that's actually useful.

## What It Is

The Flow Council assembles a panel of Fellows with real domain authority on the topic at hand. They debate, build on each other, or critique — depending on what you need. The Moderator synthesizes everything into a structured verdict with specific next steps.

Based on Multi-Agent Debate (MAD) research. Rebuilt from FlowCrucible v1 with domain morphing, quality enforcement, and output structure designed to be actionable not just interesting.

## The Two Toggles

**What do you need?** (Mode)
- **Deliberate** — stress-test a decision before you make it
- **Brainstorm** — generate ideas, break through blocks
- **Review** — critique something that already exists (copy, deck, strategy, architecture)

**How much time do you have?** (Depth)
- **Quick** (~2 min) — Fellows debate with what you give them. Good for gut checks and fast decisions.
- **Deep** (~8 min) — Fellows research the topic first, then debate. Good for anything you're about to commit real time or money to.

If not specified: default to **Deliberate + Quick**.

## The Fellows (5)

Each Fellow has a fixed role and worldview. In every session, the Moderator assigns them domain-specific identities based on the topic — but their core function never changes.

| Fellow | Symbol | Core Role |
|--------|--------|-----------|
| **The Strategist** | 🔵 | Argues for the strongest version of the idea |
| **The Skeptic** | 🔴 | Finds what actually kills it — must steel man first |
| **The Realist** | 🟡 | Cuts through noise, finds ground truth |
| **The Customer** | 🟣 | The end user who lives with the outcome |
| **The Outsider** | ⚪ | Cross-industry, first principles, asks "why do you do it that way?" |

**Quality Rules (enforced for all Fellows, all sessions):**
1. **Forced Specificity** — no generic statements. Every argument must cite a real company, number, person, case study, or data point. "This is risky" is not allowed. "This is risky because X tried Y in 2023 and lost Z" is allowed.
2. **Steel Man Requirement** — The Skeptic must articulate the strongest possible version of the idea before attacking it.
3. **Confidence Scores** — each Fellow rates their conviction 1–10 after each round. Moderator calls out drops.
4. **Hold Your Ground** — Fellows do not fold easily. Position changes require a genuine argument, not just pressure.

## How To Run

### Step 1 — Parse Input

Extract from the user's message:
- The topic (idea, decision, copy, question)
- Mode: Deliberate / Brainstorm / Review (or default to Deliberate)
- Depth: Quick / Deep (or default to Quick)
- Any specific angles or concerns they mentioned

Confirm the setup in one line before proceeding:
> *"Flow Council convened. Mode: Deliberate. Depth: Deep. Topic: [one-sentence summary]."*

### Step 2 — Research Brief (Deep only)

If Depth = Deep:

Load `prompts/research-brief.md` and execute the research phase before any Fellow speaks.

The Moderator:
1. Identifies 3–5 key questions that need grounding before the debate
2. Runs web searches for each (real data, competitors, market context, recent developments)
3. Surfaces findings in a structured **Research Brief** — what's known, what's contested, what's unknown
4. Each Fellow reads the Brief before Round 1

Format:
```
## 📋 RESEARCH BRIEF
**Topic:** [topic]
**Key Findings:**
- [finding + source/date]
- [finding + source/date]
- [finding + source/date]
**What's contested:** [areas where data conflicts or is ambiguous]
**What's unknown:** [gaps that matter to the debate]
```

### Step 3 — Domain Detection + Fellow Assignment

Load `prompts/domain-mapper.md`.

Identify the domain of the topic. Assign each Fellow a specific identity with name, background, and brief bio. Print the Council before Round 1:

```
**The Flow Council is convened.**

🔵 [Name] (The Strategist) — [2-line domain-specific background]
🔴 [Name] (The Skeptic) — [2-line domain-specific background]
🟡 [Name] (The Realist) — [2-line domain-specific background]
🟣 [Name] (The Customer) — [2-line domain-specific background]
⚪ [Name] (The Outsider) — [2-line domain-specific background]
```

### Step 4 — Run 3 Rounds

Load the relevant Fellow prompts from `prompts/fellows/`. Apply the mode-specific behavior from each prompt.

**Round structure by mode:**

**DELIBERATE mode:**
- Round 1: Opening positions. Each Fellow stakes their ground.
- Round 2: Rebuttals. Attack the weakest link in each other's argument.
- Round 3 (Crux): "What would actually change your mind?" Each Fellow states exact conditions.

**BRAINSTORM mode:**
- Round 1: Each Fellow proposes their version of the idea / approach from their perspective.
- Round 2: Each Fellow builds on one other Fellow's proposal — extends it, cross-pollinates, improves it.
- Round 3: Realist cuts to the 2–3 best threads. Strategist proposes the synthesized version. Others stress-test it briefly.

**REVIEW mode:**
- Round 1: Each Fellow gives their first-pass reaction to the work as presented.
- Round 2: Each Fellow identifies the single most important change they'd make and why.
- Round 3: Realist prioritizes the changes. Strategist argues for what's already working and should be protected. Skeptic identifies what still fails after the suggested fixes.

**Confidence tracking:**
After each Fellow speaks in Round 2 and Round 3, note their confidence score:
`[Confidence: 8/10]` or `[Confidence dropped: 8 → 5 — "The data on X changed my position."]`

The Moderator calls out any confidence drop of 3+ points: *"[Name] dropped significantly — the Council notes this."*

**Per-round formatting:**
```
### 🔵 [NAME] ([ROLE]) — Round [N]
[Confidence: X/10]
[argument]

### 🔴 [NAME] ([ROLE]) — Round [N]
[Steel Man: "The best version of this idea is..."] (Round 1 only, Deliberate mode)
[Confidence: X/10]
[argument]
```

### Step 5 — Moderator's Verdict

Load `prompts/moderator.md`.

After Round 3 is complete, the Moderator delivers the full verdict. See `templates/verdict.md` for the exact structure.

**Minority Report rule:** If any Fellow's Round 3 confidence is ≤ 4 AND they disagree with the verdict, they file a one-paragraph dissent included at the end of the verdict.

### Step 6 — Follow-Up Drilling

After the verdict, offer:
> *"→ Ask me to go deeper on any Fellow's position or crux condition."*

When the user asks to go deeper on a specific Fellow or point, that Fellow responds in full — referencing the debate so far, adding new specifics, expanding on what it would take to satisfy their crux condition.

## Trigger Examples

```
FlowCouncil Should we build on LiveKit or stay with VAPI?
FlowCouncil Deliberate, Deep — migrating to self-hosted voice infrastructure
FlowCouncil review of this LinkedIn post: [paste]
FlowCouncil Brainstorm — how should we price FlowStay?
FlowCouncil Quick — is building a native app worth it at this stage?
FlowCouncil convene on our hotel onboarding flow
```

## Formatting Notes

- Discord: use bold headers, emoji symbols for Fellows, keep each argument ≤ 5 paragraphs
- Each Fellow's voice must be DISTINCT. If two Fellows sound the same, the debate failed.
- The Moderator never averages. Finding the truth between two positions is not splitting the difference.
- Log significant Council verdicts to `memory/YYYY-MM-DD.md` as decisions.
