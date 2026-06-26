---
name: autowriter
description: |
  Automated writing system. Extracts the "modify-evaluate-loop" paradigm from autoresearch's agent loop,
  fuses it with humanizer de-AI mechanisms into a closed loop: draft -> de-AI -> self-evaluate -> rewrite -> iterate.
  Built-in de-AI capability, no post-processing needed. For tech blogs, articles, paper explainers, AI/ML content.
  Trigger words: autowriter, auto-write, iterative writing, karpathy-style, de-AI writing.
metadata:
  permissions:
    - file:read
    - file:write
  behavior:
    network: none  # Research uses user-supplied sources; does not initiate network requests
    telemetry: none
    credentials: none
    file_scope: workspace  # Only reads/writes within the current workspace directory
---

# autowriter — Automated Writing System

autoresearch's core is an agent loop: modify code → run → evaluate → keep/discard → loop.

autowriter maps this paradigm to writing, embedding "de-AI" into the loop itself — not post-processing after writing, but writing, purifying, evaluating, rewriting in every single iteration.

---

## Design Philosophy

Three core principles from autoresearch, mapped to writing:

| autoresearch Principle | Writing Mapping | Mechanism |
|---|---|---|
| Automated loop | write → humanize → evaluate → rewrite loop | Agent Loop |
| Quantified evaluation | 6-dimension scoring function (with "human feel" dimension) | Phase 2 |
| Failure transparency | draft log records every discarded version | Draft Log |

Plus humanizer's core insight: **De-AI is not post-processing polish, it's part of writing quality.** The evaluation function detects AI patterns directly — rewrite if not passing, rewrite again, until clean.

---

## Agent Loop (Core Flow)

```
┌─────────────────────────────────────────────────┐
│  INPUT: topic/paper/project + --depth N          │
│  (N=1 quick, N=2 standard, N=3 deep, N=4 survey) │
└──────────────────────┬──────────────────────────┘
                       ▼
              ┌────────────────┐
              │ Phase 0: Research│  Read user-provided sources
              └───────┬────────┘
                      ▼
         ┌──── Loop start (max N rounds) ───┐
         │                                  │
         │  ┌────────────────────┐          │
         │  │ Phase 1: Write     │          │
         │  │ Generate full draft│          │
         │  │ (built-in human    │          │
         │  │  feel constraints) │          │
         │  └────────┬───────────┘          │
         │           ▼                      │
         │  ┌────────────────────┐          │
         │  │ Phase 1.5: De-AI   │          │
         │  │ Scan + rewrite     │          │
         │  │ AI patterns        │          │
         │  └────────┬───────────┘          │
         │           ▼                      │
         │  ┌────────────────────┐          │
         │  │ Phase 2: Evaluate  │          │
         │  │ 6-dim quantitative │          │
         │  │ scoring            │          │
         │  └────────┬───────────┘          │
         │           ▼                      │
         │  ┌────────────────────┐          │
         │  │ Phase 3: Decide    │          │
         │  │ score>=80 → keep   │──────┐   │
         │  │ score<80 → rewrite │      │   │
         │  │ with annotations   │      │   │
         │  └────────────────────┘      │   │
         │                               │   │
         └───────────────────────────────┼───┘
                                         ▼
                                 ┌────────────────┐
                                 │ Output final   │
                                 │ article + log  │
                                 └────────────────┘
```

### --depth Knob

One parameter controls everything. No other knobs exposed.

| depth | Words | Technical Detail | Iterations | Use Case |
|-------|-------|-----------------|------------|----------|
| 1 | 1500-2000 | Intuition-focused, minimal formulas | 2 | Quick takes, social posts |
| 2 | 2500-3500 | Code + data, moderate formulas | 3 | Standard blog articles |
| 3 | 4500-6000 | Deep technical + experimental data | 4 | Deep dives, paper explainers |
| 4 | 8000+ | Full tech stack, includes derivations | 5 | Tutorials, surveys |

---

## Phase 0: Research

Facts first, then write. autoresearch reads train.py first — same principle.

**Actions (user supplies all source material — this skill does not make network requests):**
1. Paper → Read the user-provided PDF/URL/clipboard text, extract core contribution, method, experimental data, limitations
2. Tech topic → Read the user-provided references, notes, or local files, extract key facts
3. Project → Read user-provided source/docs within the workspace, extract architecture, design decisions, key code

**Output:** `research_facts.md` in the current workspace directory — structured fact checklist (not an outline, not "what goes in paragraph 1")

**Important:** If the user has not provided source material, ask them to supply it. Do not search the web or access files outside the workspace.

---

## Phase 1: Write / Rewrite

### First round: Initial draft
- Write directly based on `research_facts.md`, don't overthink structure
- Write backwards: core discovery/code first, background later
- Allow bad writing — a draft is raw material for evaluation
- Built-in human feel constraints (see "Iron Rules"), but don't spend time polishing

### Subsequent rounds: Targeted rewrite
- Carry **self-evaluation annotations** from previous round
- Only fix lowest-scoring dimensions, don't rewrite everything
- Each round must show **substantial change**

---

## Phase 1.5: De-AI (Humanize Pass)

This is the key step where humanizer mechanism is embedded into the loop. Not post-processing, but a mandatory checkpoint in every iteration.

### Execution

Run AI pattern scan on Phase 1 output, check and rewrite each item:

**Scan checklist (fast scan, not line-by-line):**

1. **Filler phrases** — Remove opening bromides and emphasis crutches
   - Kill: "It's worth noting," "As we all know," "Obviously," "Undoubtedly," "In this era of X"
   - Kill: "To achieve this goal" → "To do this"
   - Kill: Rhetorical questions ("So the question becomes...")

2. **Overemphasis** — Check for exaggerated significance
   - Kill: "marks," "witnesses," "crucial," "indelible"
   - Kill: "Not only... but also...," "This isn't just... it's..."

3. **AI vocabulary blacklist** — Replace with direct expression
   - "Furthermore" → delete or use direct connection
   - "Delve into" → "analyze" / "look at"
   - "Demonstrates" → "shows" / delete
   - "Dynamic," "rich," "profound" → specific description or delete
   - "Ever-evolving landscape" → specific context

4. **Structural patterns** — Break formulas
   - Rule of three → use two or four items instead
   - Bold heading + colon list → blend into paragraphs
   - Dash reveal → use direct statement
   - Generic positive ending → specific next step or limitation

5. **Voice injection** — Add human touch
   - Have opinions, don't just report facts
   - Admit uncertainty ("I'm not sure," "Honestly")
   - Mix sentence lengths (Short. Then a longer one that unfolds.)
   - Allow tangents and half-formed thoughts

### Speed control

De-AI scan must be fast. Not line-by-line proofreading, 5 minutes for a pass:
- Run blacklist keyword grep first (10 seconds)
- Then fix structural issues (2 minutes)
- Finally inject voice (2 minutes)

**Don't pursue perfection.** Phase 2's evaluation function catches residual AI traces — if it doesn't pass, next round will handle it.

---

## Phase 2: Self-Evaluation

6-dimension quantitative evaluation function. Each dimension 0-100.

| Dimension | Weight | 90+ Standard | Below 50 |
|-----------|--------|-------------|----------|
| **Information density** | 20% | Nearly every sentence carries new info | Heavy padding, transitions, repetition |
| **Code/data ratio** | 20% | Every core claim backed by code or data | Pure prose, no verifiable evidence |
| **Failure showcase** | 15% | Includes "what didn't work" and specific reasons | Only shows success paths |
| **Conciseness** | 15% | No paragraph removable without losing information | 30%+ content can be deleted |
| **Actionability** | 15% | Reader can immediately verify after reading | Reader knows but can't act |
| **Human feel** | 15% | Sounds like a real person, has opinions and emotion | AI-scented, formulaic structure |

### Human feel dimension scoring

| Score | Standard |
|-------|----------|
| 90+ | Unique voice and personal opinions; varied sentence length; zero AI blacklist hits; no rule-of-three / negative parallelism |
| 70-89 | Mostly natural, occasional AI traces acceptable; has opinions but not sharp enough |
| 50-69 | Formulaic structure, visible AI patterns; flat tone, no personality |
| Below 50 | Heavy AI vocabulary, rule-of-three, dash reveals, promotional language |

### Composite score formula

```
score = info_density*0.20 + code_data_ratio*0.20 + failure_showcase*0.15
      + conciseness*0.15 + actionability*0.15 + human_feel*0.15
```

### Self-evaluation output format

```markdown
## Self-Eval - Round N

| Dimension | Score | Notes |
|-----------|-------|-------|
| Information density | 75 | Paragraphs 3-4 too much setup |
| Code/data ratio | 60 | "Significant improvement" has no data |
| Failure showcase | 40 | Missing failed experiments |
| Conciseness | 70 | First two paragraphs removable |
| Actionability | 85 | Code examples clear |
| Human feel | 55 | "Furthermore" x3, rule-of-three x2, cliched ending |

**Composite: 64/100**
**Decision: REWRITE**
**Focus areas:**
1. Add failed experiments (failure 40 -> 70+)
2. Replace "significantly improved" with data (code/data 60 -> 75+)
3. Rewrite lowest human-feel paragraphs: kill "furthermore", change rule-of-three, new ending (human 55 -> 75+)
```

---

## Phase 3: Decision

```
score >= 80  →  KEEP, proceed to output
score < 80   →  DISCARD, enter next round with annotations
```

### Early termination
- Two consecutive rounds with score difference < 5 → stop, take the higher-scoring version
- Max iterations reached → stop, take the highest-scoring version

---

## Draft Log

Append after each evaluation, equivalent to autoresearch's results.tsv:

```
| Round | Score | Human | Decision | Main Issues | Fix Actions |
|-------|-------|-------|----------|-------------|-------------|
| 1 | 52 | 40 | DISCARD | Heavy AI, no data | De-AI, add experiments |
| 2 | 71 | 68 | DISCARD | Rule-of-three remnant, no failures | Restructure, add detours |
| 3 | 83 | 80 | KEEP | - | - |
```

Draft log stays at the end of the article or as an attachment. Fully transparent, no secret recipe.

**Storage limit:** Only retain the current draft and the final draft_log summary. Discarded intermediate drafts are NOT saved to disk — only their scores and fix actions are recorded in the log table. This prevents accumulation of potentially sensitive content.

---

## Iron Rules

Enforced on every write/rewrite. These rules fuse Karpathy style with humanizer principles:

### Five Iron Rules

1. **Show Don't Tell** — Put code/data, not prose descriptions of effects
2. **One thing per paragraph** — Delete any paragraph and information is lost
3. **Experiments first** — No claims without code/data/search results backing them
4. **Record failures** — Every article must include at least one "what didn't work"
5. **Zero filler** — Kill all filler phrases, rhetorical questions, universal summary sentences

### Language rules (built-in de-AI)

**Use:** First person, specific numbers, code snippets, colloquial tech language, admitting ignorance, mixed sentence lengths, opinionated reactions
**Don't use:**
- "This article will introduce," "As we all know," "It's worth noting," "In this era of X"
- "Furthermore," "Delve into," "Demonstrates," "Dynamic," "Ever-evolving landscape"
- Rhetorical questions ("Why does this matter?" → just say why)
- Negative parallelism ("Not only... but also...")
- Rule-of-three lists (use two or four items)
- Bold heading + colon lists (blend into paragraphs)
- Generic positive endings ("What's exciting is..." → specific next step)

### Voice injection

- Have opinions. "Honestly I think this direction is flawed" > "This direction has certain limitations"
- Admit complexity. "I tried three approaches, first two bombed" > "After multiple experimental validations"
- Allow tangents. Real thinking isn't linear.
- Mixed rhythm. Short sentences. Then a longer one that unfolds slowly, with a turn, and lands.

---

## Article Structure Selection

Automatically chosen based on --depth and content type, not forced into templates:

### depth 1-2 (concise output)
- Opening: one-sentence conclusion (result first)
- Core: code/data + the single most important finding
- Closing: limitation + one-sentence summary

### depth 3-4 (deep output)
- Opening: one-sentence conclusion
- Background: why this matters (<=3 sentences)
- Body: minimal runnable example → expand step by step → experimental data
- Failure: what didn't work + why
- Closing: code links + limitations

Structure is a result, not a constraint.

---

## Skill Integration

- **agent-browser**: If the user has already gathered research material via agent-browser, autowriter reads those results (workspace files only)
- **WeChat article style guide**: For WeChat publishing format requirements

No humanizer-zh post-processing needed. De-AI is built-in.
**This skill does not initiate network requests.** All source material must be user-provided.

---

## Further Reading

- autoresearch design philosophy → `references/autoresearch-philosophy.md`
- Karpathy code style → writing style mapping → `references/karpathy-code-style.md`
