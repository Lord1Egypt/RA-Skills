---
name: game-dev-brainstorm
description: >
  Game concept ideation using MDA framework, verb-first design, and mashup
  method. Guides the developer through a structured 6-phase brainstorming
  process to produce a viable game concept.
triggers:
  - "I need a game idea"
  - "brainstorm game concepts"
  - "what game should I make?"
  - "game design ideas"
  - "concept ideation"
---

# Game Dev Brainstorm — Concept Ideation

## 🎯 Purpose

Go from blank page to a validated game concept with a defined core loop,
design pillars, and scope commitment. Uses structured creative methods rather
than random idea generation.

## 🤖 Multi-Platform Notes

| Platform | Notes |
|----------|-------|
| **OpenClaw** | Best for this skill. Can hold multi-turn conversations, create files, save outputs. Each phase can produce a persistent artifact. |
| **Claude Code** | Good for text output and file creation. Works best if user types answers. Use `echo` / `cat` to create concept files. |
| **Cursor/Windsurf** | Chat panels work well. Concept outputs can be saved alongside project. |
| **GitHub Copilot** | Chat can handle basic Q&A. Good for filling out templates. |
| **Generic LLM Chat** | All can do this. Output concept notes and ask the user to save them. |
| **Any AI** | This skill is universal — no file operations needed for the creative phase, just structured Q&A. Save results when done. |

**Save outputs** as `game-dev-studio/brainstorm-output.md` when on a platform
that supports file writing (OpenClaw, Claude Code, Cursor).

---

## 🧭 Phase 1: Creative Discovery

### Step 1.1 — Inspiration Mining

Ask the user:

> **"What games, movies, books, or experiences have inspired you recently?"**
>
> List 2-5. Don't judge, just list. Include things you love AND things you
> hate (hate can be just as inspiring).

### Step 1.2 — Emotion Target

Ask:

> **"What feeling do you want players to have?"**
>
> Examples: wonder, tension, satisfaction, curiosity, dread, pride, flow,
> relaxation, discovery, mastery, social connection.

**Write down:** 1-3 primary emotion targets.

### Step 1.3 — Constraint Setting

Ask:

> **"What constraints are we working with?"**
>
> - **Time:** [1 week / 1 month / 3 months / 6+ months]
> - **Team:** [solo / 2-3 / 5+]
> - **Skills:** [programming / art / audio / design]
> - **Budget:** [$0 / $100 / $1000+]
> - **Target platform:** [PC / Mobile / Web / Console]

---

## 💡 Phase 2: Concept Generation

### Step 2.1 — Mashup Method

Take 2-3 inspirations from Phase 1 and force-combine them:

> "What if **Dark Souls** had the exploration of **Breath of the Wild** and
> the crafting of **Stardew Valley**?"

Use this template:

```
[Game A] + [Game B with mechanic/feel] = [new concept]
```

Generate 3-5 mashups. Don't filter yet.

### Step 2.2 — Verb-First Design

For each mashup, define the **primary verbs** (what the player actually does):

| Mashup | Primary Verbs |
|--------|---------------|
| Example | run, jump, dash, collect, craft, defend |

Good verbs are active, physical, and repeatable. "Explore" is vague. "Grapple"
is specific.

**Rule:** If you can't list 3-5 concrete verbs, the concept isn't actionable.

### Step 2.3 — Player Fantasy

Ask:

> **"Who is the player pretending to be?"**
>
> Examples: A ghost haunting a spaceship. A gardener who fights demons.
> A postal worker in a post-apocalyptic wasteland.

### Step 2.4 — Concept Pitch

For the 1-2 strongest mashups, write a one-sentence pitch:

> *"It's [Genre] where you [Core Verb] to [Goal] in a [Setting]."*
>
> Example: *"It's a 2D platformer where you magnetically swap polarity to
> navigate a collapsing space station."*

---

## 🔄 Phase 3: Core Loop Design

### Step 3.1 — Define the Core Loop

The core loop is what the player does every ~30 seconds to ~5 minutes.

Draw this as:

```
[Action] → [Reward] → [Progression] → [New Action]
```

Example (action platformer):
```
[Jump across gap] → [Reach platform] → [New power-up] → [Jump bigger gaps]
```

Example (farming sim):
```
[Plant seeds] → [Water daily] → [Harvest crop] → [Sell for better seeds]
```

Ask the user to describe their loop. Help them shorten it if it's too long.

### Step 3.2 — Define the Progression Loop

The progression loop is what happens over hours/sessions:

```
[Session Goal] → [Unlock] → [New Content] → [Bigger Challenge]
```

---

## 🏛️ Phase 4: Design Pillars

Define 3-5 **non-negotiable** pillars. These guide every decision.

Pillar format:

> **[Pillar Name]** — [One sentence describing what it means]
>
> - ✅ [What this looks like when done right]
> - ✅ [Another example]
> - ❌ [What this is NOT]
>
> **Scope anchor:** [How this keeps scope in check]

**Example pillars:**

| Pillar | Statement |
|--------|-----------|
| **Tight Controls** | Every input gives instant, satisfying feedback. No input lag. |
| **Emergent Story** | The narrative emerges from gameplay, not cutscenes. |
| **Pick-up-and-Play** | No tutorial needed. One-screen teaches everything. |
| **Cozy Vibez** | Warm colors, gentle music, no fail states. |

### Pillar Scope Check

For each pillar, ask:

> **"Does this pillar help us cut features or add them?"**

Pillars should help **cut** features. If every pillar adds scope, revise.

---

## 🎮 Phase 5: Player Validation

### Step 5.1 — Player Profile

Ask:

> **"Who is this for?"**
>
> ```
> 1) Casual — 15 min sessions, mobile/switch
> 2) Core — 1-2 hour sessions, PC/console
> 3) Hardcore — marathon sessions, deep systems
> 4) Spectator — fun to watch, streamer-friendly
> ```

### Step 5.2 — One-Sentence Hook

Ask the user to pitch the game in one sentence that makes someone say "I want
to play that."

> *"You're a raccoon running a space café who must steal ingredients from
> alien planets."*

### Step 5.3 — Feasibility Check

Rate the concept on a 1-5 scale:

```
Originality:    [1-5]
Feasibility:    [1-5]  (can WE build this?)
Fun Potential:  [1-5]
Scope Risk:     [1-5]  (5 = dangerous)
```

If Scope Risk > Feasibility, scale down.

---

## ✂️ Phase 6: Scope

### Step 6.1 — Minimum Viable Game

Define the absolute minimum to be fun:

> **"What is the smallest playable version of this that is still fun?"**

List only the essentials:
- 1 level
- 2 enemy types
- 1 weapon
- Core mechanic working

### Step 6.2 — Scope Buckets

```
MVP (Day 1)         | V1 (Week 1)        | V2 (Month 1)       | Stretch
--------------------|--------------------|--------------------|--------------------
Core movement       | Tutorial level     | 3 more levels      | Multiplayer
1 enemy type        | 2 more enemy types | Boss fight         | Leaderboards
Basic UI            | Settings menu      | Save/load          | Achievements
Win/lose condition  | Sound effects      | Music              | Cutscenes
```

### Step 6.3 — Commitment

Ask the user to commit to **one** concept. Save the output.

---

## 📄 Output Template

After completing all phases, write `brainstorm-output.md`:

```markdown
# Brainstorm Output

## Pitch
[One-sentence hook]

## Core Loop
[Verb] → [Reward] → [Progression] → [New Action]

## Design Pillars
1. [Pillar 1]
2. [Pillar 2]
3. [Pillar 3]

## Player Profile
[Casual / Core / Hardcore / Spectator]

## MVP Scope
- [ ] Essential feature 1
- [ ] Essential feature 2
- [ ] Essential feature 3
- [ ] Essential feature 4

## Constraints
- **Time:** [X]
- **Team:** [X]
- **Engine:** [X]

## Next Steps
→ Run `game-design-doc` to write the GDD
→ Run `setup-engine` to configure the engine
→ Run `prototype` to validate a risky mechanic
```
