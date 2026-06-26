# PM Agent — Framework Reference

Quick-reference for the 7 classic PM frameworks used in this skill.

## 1. Jobs-to-be-Done (JTBD)

**Author:** Clayton Christensen (Harvard Business School)

**Core idea:** Customers don't buy products — they "hire" them to get a job done.

**Interview structure:**
1. "Tell me about the last time you [solved this problem]."
2. Walk through the timeline: trigger → search → decide → use → outcome
3. Map the forces:
   - **Push:** Pain with current situation (drives away)
   - **Pull:** Attraction of new solution (draws toward)
   - **Anxiety:** Fear of change (holds back)
   - **Habit:** Attachment to status quo (holds back)

**Output:** Job statement format: "When [situation], I want to [motivation], so I can [expected outcome]."

---

## 2. Opportunity Solution Tree

**Author:** Teresa Torres (Continuous Discovery Habits)

**Structure:**
```
Desired Outcome (measurable business goal)
├── Opportunity 1 (user need/reason)
│   ├── Solution A
│   ├── Solution B
│   └── Solution C
├── Opportunity 2
│   ├── Solution D
│   └── Solution E
└── Opportunity 3
    └── Solution F
```

**Rules:**
- Opportunities come from research, not invention
- One outcome, many opportunities, many solutions per opportunity
- A solution without an opportunity is a feature without a reason
- Keep iterating: failed solutions → new opportunities → new solutions

---

## 3. RICE Scoring

**Use case:** Prioritizing features/backlog items

| Factor | Scale | What it means |
|--------|-------|---------------|
| **R**each | Users/time period | How many users affected in a quarter |
| **I**mpact | 0.25 (minimal) → 3 (massive) | How much it moves the needle |
| **C**onfidence | 50% → 100% | How sure are you about the estimates |
| **E**ffort | Person-months | Total team effort to ship |

**Formula:** Score = (R × I × C) / E

**Example:** Reach 1000 users × Impact 2 × Confidence 80% / Effort 2 months = 800

---

## 4. Kano Model

**Use case:** Categorizing features by user satisfaction impact

| Category | Without it | With it | Strategy |
|----------|-----------|---------|----------|
| **Must-have** | Frustrated | Neutral | Ship it, don't brag |
| **Performance** | Dissatisfied | Satisfied (proportional) | Invest and optimize |
| **Delighter** | Neutral | Delighted | Differentiate here |
| **Indifferent** | Nothing | Nothing | Don't build |

**Survey method:** Ask two questions per feature:
- "If this feature existed, how would you feel?" (functional)
- "If this feature didn't exist, how would you feel?" (dysfunctional)

---

## 5. Amazon Working Backwards (PRD)

**Source:** Amazon internal methodology

**Step 1 — Press Release (1 page)**
Write as if the product launched TODAY:
- **Heading:** Name + one-line benefit
- **Sub-heading:** Who benefits and how
- **Summary:** What it does in 2-3 sentences
- **Problem:** The pain it solves
- **Solution:** How it works
- **Quote:** From a fictional (but realistic) happy customer
- **How to get started:** Simple first step
- **Closing:** Vision for the future

**Step 2 — FAQ**
- External FAQ: What will customers ask?
- Internal FAQ: What will engineers/leadership ask?

**Step 3 — Tenets**
3-4 guiding principles. Example:
- "Customer obsession over competitor obsession"
- "Data-informed, not data-paralyzed"

---

## 6. Google Design Sprint

**Author:** Jake Knapp (Google Ventures)

**5-day structure:**

| Day | Phase | Activities | Output |
|-----|-------|-----------|--------|
| Mon | **Map** | Define challenge, pick target, map user journey | Long-term goal + sprint questions |
| Tue | **Sketch** | Lightning demos, Crazy 8s, solution sketches | 3-8 rough concepts |
| Wed | **Decide** | Art museum, heat map, speed critique, straw poll | Winning concept + storyboard |
| Thu | **Prototype** | Build realistic-enough prototype | Clickable prototype |
| Fri | **Test** | 5 user interviews, 1:1 sessions | Pattern report + next steps |

**Key insight:** 5 users catch 85% of usability problems (Nielsen's research).

---

## 7. Lean Startup BML Cycle

**Author:** Eric Ries

```
    Idea
      ↓
   Build ──→  Measure  ──→  Learn
      ↑                       │
      └───────────────────────┘
         (iterate or pivot)
```

**Experiment template:**
- **Hypothesis:** We believe [X]. We'll know it's true when [metric] reaches [threshold].
- **MVP:** Smallest thing to test (smoke test, fake door, concierge, Wizard of Oz)
- **Metric:** One primary metric, defined BEFORE building
- **Timebox:** Fixed duration, then decide: persevere or pivot

**Pivot types:**
1. Zoom-in pivot (one feature → whole product)
2. Zoom-out pivot (whole product → one feature)
3. Customer segment pivot (same product, different user)
4. Customer need pivot (same user, different problem)
5. Platform pivot (app → platform or vice versa)
6. Business architecture pivot (complex ↔ simple)
7. Value capture pivot (how you monetize)
8. Engine of growth pivot (viral ↔ sticky ↔ paid)
9. Channel pivot (how you reach customers)
10. Technology pivot (same solution, different tech)

---

## Framework Selection Guide

| Question | Framework |
|----------|-----------|
| What problem should we solve? | JTBD + Opportunity Solution Tree |
| Which problem first? | RICE + Kano |
| How to write clear requirements? | Amazon Working Backwards |
| How to validate fast? | Design Sprint + Lean BML |
| How to measure success? | OKR |
| How to connect discovery to delivery? | Dual-Track Agile |
