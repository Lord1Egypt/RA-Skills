---
name: "concept-decoder"
description: "Deconstructs complex concepts with a layered, intuition-first pipeline (prereqs → motivation → analogies → math → connections → tests). Use when user asks 'what is X', wants intuition behind formulas, or feels stuck."
---

# Concept Decoder

---

## Overview

This skill systematically deconstructs complex, abstract, or formula-heavy scientific concepts — from quantum mechanics to abstract algebra to statistical physics — using a first-principles cognitive pipeline. It transforms opaque jargon into layered, intuitive understanding by reversing the textbook order: motivation before formalism, analogy before algebra, connection before isolation.

**Language policy:** Respond in the same language the user writes in. If the user writes in Chinese, deliver the full decode in Chinese. If in English, in English. For mixed input, default to English.

---

## When to Use This Skill

Use `/decode` or trigger this skill when:

- User encounters a concept that feels "opaque" (e.g., replica symmetry breaking, spinor, adjoint functor)
- The concept is formula-heavy and the user wants intuition behind the math
- The concept spans multiple layers of abstraction (e.g., requires understanding 3+ prerequisite ideas)
- User says things like "what really is X?", "explain X from scratch", "I never truly understood X"

**Do NOT use this skill when:**
- The user only needs a quick definition lookup (use direct answer instead)
- The concept is elementary and the user is already expert-level (ask first)

---

## Depth Levels

The user can specify a depth level in the trigger command. Default is **Standard**.

| Level | Trigger Syntax | Layers Covered | Approx. Length |
|-------|---------------|----------------|----------------|
| **Quick** | `/decode X, quick` | Layers 1–2 only | ~500 words |
| **Standard** | `/decode X` *(default)* | Layers 0–5 | ~1500–2500 words |
| **Deep** | `/decode X, deep` | All 6 layers | ~3000–5000 words |

Examples:
```
/decode Laplacian operator
/decode replica symmetry breaking, deep
/decode group theory, quick
/decode 拉普拉斯算子
/decode 复本对称破缺，深度模式
```

---

## Core Philosophy

> **"You don't understand something until you can explain what problem it solves for someone who has never heard of it."**

Three anti-patterns this skill avoids:
1. ❌ Starting with the formal definition (this is how textbooks lose people)
2. ❌ Skipping the "why" and jumping to "how" (formulas without motivation are dead symbols)
3. ❌ Treating the concept in isolation (understanding = connecting to what you already know)

---

## Workflow: The Six-Layer Deconstruction

### Layer 0: Prerequisite Scan
**[STOP POINT — present the tree, then WAIT for user response before proceeding]**

Before deconstruction begins:

- **Identify the concept** and its home domain (e.g., "RSB" → statistical physics → disordered systems)
- **List prerequisite concepts** as a dependency tree:
  ```
  Example for RSB:
  RSB
  ├── Replica trick
  │   ├── Partition function Z
  │   │   └── Statistical mechanics basics
  │   └── Quenched vs. annealed disorder
  ├── SK model
  │   ├── Ising model
  │   └── Mean-field theory
  ├── Order parameter (overlap q)
  │   └── Spontaneous symmetry breaking
  └── Free energy landscape
      └── Metastability
  ```
- **Ask the user**: "Here are the prerequisite layers. Which ones are you comfortable with? I'll skip those and focus on the gaps."
- **Wait for response** before proceeding to Layer 1.

**If prerequisite gaps are too large (5+ unknown concepts):**
- Propose a "learning ladder": offer to decode prerequisites first in recommended order
- Offer a rapid (Layers 1+2 only) pass on each prerequisite before tackling the target

---

### Layer 1: The Problem — Why Does This Concept Exist?

Every concept was invented to solve a problem. Start there.

**Template:**
> Before [CONCEPT] existed, people tried to understand [PHENOMENON].
> The existing tools ([PREVIOUS APPROACHES]) failed because [SPECIFIC FAILURE].
> [CONCEPT] was introduced by [WHO, WHEN] to resolve this failure.

**Requirements:**
- Describe the **concrete physical/mathematical situation** that demanded this concept
- Show what goes **wrong** without it (a failed calculation, a paradox, an inconsistency)
- Make the user **feel the pain** of not having this concept

**Example for RSB:**
> Sherrington and Kirkpatrick (1975) proposed a mean-field model for spin glasses.
> Applying the replica trick with the simplest assumption — that all replicas are equivalent
> (replica symmetric, RS) — gives a free energy that yields **negative entropy** at low temperature.
> This is physically absurd. Something in the RS assumption must be wrong.
> Parisi (1979) realized: the replicas are NOT equivalent — their symmetry is **broken**.

---

### Layer 2: The Intuitive Picture — Analogy Before Algebra

Provide **at least two analogies** at different levels:

1. **Everyday analogy** (for the "aha" moment):
   - Must be concrete, visual, experiential
   - Acceptable to be imperfect — explicitly state where the analogy breaks down

2. **Cross-domain scientific analogy** (for structural understanding):
   - Map the concept to a parallel structure in a domain the user already knows
   - Highlight what is structurally identical and what differs

**Requirements:**
- Every analogy **must** include a **"Where this analogy breaks"** disclaimer
- Use analogies to build intuition, then **immediately** show how the real concept is richer

**Example for RSB:**
> **Everyday analogy:** Imagine a mountain landscape with many valleys. A ball rolling
> on this landscape gets trapped in whichever valley it falls into — not necessarily the
> deepest one. RS assumes there's essentially one valley. RSB says: no, there's a
> **hierarchy** of valleys within valleys within valleys, like a fractal.
>
> **Where it breaks:** Real spin glass landscapes have ultrametric structure
> (the "distance" between valleys obeys a tree metric), which has no everyday counterpart.

---

### Layer 3: The Mathematical Skeleton — Formulas as Sentences

Now introduce the math, but treat **every formula as a sentence that says something**.

**Protocol — for each key equation, provide THREE things:**
1. **The formula itself** (properly typeset in LaTeX)
2. **What it says in words** (one sentence, no jargon)
3. **What each symbol "wants to be"** (physical/geometric meaning)

Build formulas **incrementally**: start from the simplest version, add complexity one term at a time. Mark the critical step with ⚡.

**Structure:**
```
Step 1: [Simplest relevant equation]
        Words: ...
        Symbols: ...

Step 2: [Add one layer of complexity]
        Words: ...
        What changed and why: ...

    ⚡ Step 3: [The key equation where the concept lives]
        Words: ...
        THIS is where [CONCEPT] enters — because ...

Step 4: [Consequence / result]
        Words: ...
        This tells us: ...
```

**Requirements:**
- Maximum **6–8 equations** total — ruthlessly select the essential ones
- If a derivation has 20 steps, show the 4 that carry the conceptual weight; cite a reference for the rest
- Always connect back to Layer 1: "Remember the problem of [X]? Here's where it gets resolved: [equation]"

**Citation format for references:** Author(s), *Title*, Journal/Book, Year. (e.g., Parisi, G., *Order parameter for spin glasses*, PRL, 1983.)

---

### Layer 4: The Concept Map — Connections and Boundaries

Place the concept in its relational network across four directions:

| Direction | Question to answer |
|-----------|-------------------|
| **4a. Upward** (generalizations) | What broader framework contains this concept? What is it a special case of? |
| **4b. Downward** (special cases) | What are the simplest non-trivial examples? What does it reduce to in limits? |
| **4c. Lateral** (surprising links) | Where does the same mathematical structure appear in completely different fields? |
| **4d. Boundary** (where it breaks) | Under what conditions does this concept fail? What replaces it beyond those boundaries? |

**Output format:** Prefer a structured text map; offer a Mermaid diagram for complex dependency networks.

```
Example for RSB:
Generalizes:   Spontaneous symmetry breaking (but in replica space, not physical space)
Special case:  1-step RSB (simplest non-trivial case; applies to some structural glasses)
Lateral link:  Ultrametricity in RSB ↔ Taxonomy trees in biology ↔ p-adic numbers in number theory
Boundary:      RSB is a mean-field result; in finite dimensions, the droplet model may apply instead
```

---

### Layer 5: The Litmus Tests — Do You Really Understand It?

Provide **three diagnostic questions** of increasing depth. Hide answers behind spoiler markers.

| Test | Type | Purpose |
|------|------|---------|
| **Q1** | Explain-to-a-friend | Tests conceptual grasp of Layer 1–2 |
| **Q2** | Modify-one-thing | Tests structural understanding of Layer 3 |
| **Q3** | Cross-domain transfer | Tests depth of Layer 4 connections |

**Failure routing:**
- Cannot answer Q1 → revisit Layers 1–2
- Cannot answer Q2 → revisit Layer 3
- Cannot answer Q3 → revisit Layer 4

**Example for RSB:**

> **Q1:** If replica symmetry were NOT broken, what physically absurd thing would happen?
> <details><summary>Check answer</summary>Negative entropy at low T in the SK model — thermodynamically impossible.</details>

> **Q2:** What changes in the Parisi solution if you go from full RSB to 1-step RSB?
> <details><summary>Check answer</summary>The continuous order parameter function q(x) becomes a step function with a single jump.</details>

> **Q3:** Why does the same ultrametric structure appear in both spin glasses and combinatorial optimization?
> <details><summary>Check answer</summary>Both involve rugged free energy / cost landscapes with hierarchical valley structure; the ultrametric distance measures how "different" two solutions are at each level of the hierarchy.</details>

---

### Layer 6 (Optional): Historical and Human Context

**Trigger condition:** Activate automatically in **Deep** mode, or when the user explicitly asks "who invented this?" / "what's the history?"

For concepts with rich intellectual history, cover:
- **The human story**: Who invented it? What were they struggling with? What wrong paths did they try first?
- **The controversy**: Was it accepted immediately or debated? (RSB was controversial for decades; Parisi's proof of the Parisi formula was only completed by Guerra & Toninelli in 2002 and Talagrand in 2006.)
- **The legacy**: How did it reshape the field? What new questions did it open?

This layer provides the "glue" that makes a concept memorable and situates it in the living tradition of science.

---

## Formatting Standards

### Math Rendering
- Use LaTeX-compatible notation throughout
- Display equations: centered, numbered if referenced later in the text
- Inline math: for symbols embedded within sentences
- Prefer `$$...$$` for display math, `$...$` for inline

### Visual Aids
- Use ASCII/text trees for dependency and concept maps (quick to render, universally readable)
- Use Mermaid diagrams for complex multi-node networks when the user's platform supports it
- For concepts that benefit from visualization, **describe** what the figure would look like:
  > *"Imagine a plot of q(x): it's a monotonically increasing staircase function on x ∈ [0,1], with the RS solution being the degenerate case of a single step at x = 0."*

### Length Calibration
- **Quick** (Layers 1–2): ~500 words — the "aha" version
- **Standard** (Layers 0–5): ~1500–2500 words — default
- **Deep** (All 6 layers): ~3000–5000 words — full treatment

---

## Error Handling

### Concept is too broad
- Example: "Explain quantum mechanics"
- Response: Break into sub-concepts, ask user which aspect to decode first; suggest a learning path

### Concept has no clear consensus
- Example: Interpretations of quantum mechanics
- Response: Present the landscape of views, label each with its assumptions; explicitly avoid false resolution

### User's prerequisite gaps are too large
- Triggered when Layer 0 reveals 5+ unknown prerequisite concepts
- Response: Propose a "learning ladder" — decode prerequisites in recommended order; offer rapid (Layers 1+2) passes on each

### Concept is already well-known to the user
- Example: User says "I know what a derivative is, but explain the Fréchet derivative"
- Response: Acknowledge the baseline, skip to Layer 4 (lateral connections and boundary conditions) to add genuine value beyond what they already know

---

## Examples

### Example 1: Quick decode
```
User: /decode Laplacian operator, quick
→ Layer 1: "The Laplacian measures how much a function at a point differs from its
   neighborhood average. It was needed because gradient alone couldn't capture
   'local curvature in all directions simultaneously'."
→ Layer 2: Analogy — "If you're colder than your neighbors, heat flows in (∇²T > 0).
   If warmer, heat flows out (∇²T < 0). ∇²T = 0 means thermal equilibrium locally."
   Cross-domain: "In image processing, the Laplacian detects edges — pixels that
   differ sharply from their neighbors."
   Where it breaks: "Works cleanly for scalar fields; for vector fields, acts component-wise."
```

### Example 2: Deep decode
```
User: /decode replica symmetry breaking, deep
→ Full 6-layer treatment:
   Layer 0: Prerequisite tree (Ising model, mean-field theory, replica trick, ...)
   Layer 1: SK model → RS assumption → negative entropy paradox
   Layer 2: Fractal valley landscape analogy + optimization landscape cross-link
   Layer 3: Parisi ansatz, q(x) order parameter function, ultrametricity ⚡
   Layer 4: RSB ↔ p-adic numbers ↔ taxonomy trees ↔ constraint satisfaction
   Layer 5: Three litmus tests with spoiler answers
   Layer 6: Parisi (1979) → controversy → Guerra/Talagrand proof (2002–2006) → legacy
```

---

## Notes

- This skill is **purely instructional** — it generates explanations, not code or data
- For formula-heavy concepts, prioritize **conceptual clarity over derivational completeness**
- Always cite at least one key reference (seminal paper or standard textbook) per concept so the user can go deeper
- **Adapt vocabulary** to the user's background as inferred from the Layer 0 interaction — a physicist and a biologist asking about "entropy" need different entry points
- This skill does **not** require any external tools or API calls; it runs entirely on the model's language capabilities

---

## Input/Output

### Input
- A target concept (word/phrase) and optional context (domain, what the user already knows, what is confusing).
- Optional depth preference (quick / standard / deep).

### Output
- A structured explanation following the six-layer workflow, calibrated to the user’s background and requested depth.
- A small prerequisite map, clear intuition, minimal essential equations (if relevant), concept connections, and litmus-test questions.
