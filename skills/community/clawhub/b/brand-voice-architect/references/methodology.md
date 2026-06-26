# Technical Methodology Reference

## Table of Contents
1. [The 4-Pillar Framework](#1-the-4-pillar-framework)
2. [Cadence Analysis](#2-cadence-analysis-the-rhythmic-metric)
3. [Semantic Salience](#3-semantic-salience)
4. [Human-AI Collaborative Loop](#4-human-ai-collaborative-loop)
5. [Scoring Rubric](#5-scoring-rubric)
6. [This-Not-That Logic Gates](#6-this-not-that-logic-gates)

---

## 1. The 4-Pillar Framework

Every brand voice is mapped across four axes to define its **Safe Operating Area**. Plot the brand on each spectrum to produce a voice fingerprint.

| Axis | Left Pole | Right Pole |
|------|-----------|------------|
| **Character** | Friendly | Authoritative |
| **Tone** | Humorous | Serious |
| **Language** | Simple | Complex |
| **Purpose** | Helpful | Entertaining |

**Usage:** Rate each axis 1–10. A brand scoring (Character: 8, Tone: 7, Language: 9, Purpose: 3) is highly authoritative, serious, complex, and utility-focused — i.e., a technical B2B SaaS brand.

**Safe Operating Area:** Define min/max on each axis. Content outside these bounds is flagged in audits.

---

## 2. Cadence Analysis (The Rhythmic Metric)

Cadence is measured as the **standard deviation of sentence lengths** (σ).

| σ Range | Signal | Typical Use |
|---------|--------|-------------|
| 0–3 | Ultra-stable | Legal, medical, technical documentation |
| 4–6 | Balanced | B2B SaaS, editorial journalism |
| 7–10 | Dynamic | Lifestyle brands, storytelling, social media |
| 10+ | Erratic | Poetry, experimental writing |

**Average Sentence Length (ASL)** benchmarks:

| Style | ASL |
|-------|-----|
| Simple / Consumer | 10–13 words |
| Editorial / B2B | 14–18 words |
| Academic / Technical | 20–30+ words |

**Cadence Matching:** When `/audit` is run, cadence variance and ASL from the reference corpus are compared against the output. Deviations > 20% flag a cadence mismatch.

---

## 3. Semantic Salience

The goal is to identify the **top 1% of a brand's unique vocabulary** — the "Semantic Moat" that competitors cannot easily mimic.

**Process:**
1. Collect 5,000+ words of brand corpus (website copy, emails, marketing, documentation)
2. Run `voice_analyzer.py` to extract keyword frequency
3. Remove stop words and generic business vocabulary
4. The remaining high-frequency, domain-specific terms form the **Semantic Core**

**Salience Tiers:**

| Tier | Definition | Example |
|------|------------|---------|
| **Anchor nouns** | Brand-defining category terms | "precision", "protocol", "framework" |
| **Action verbs** | How the brand *does* things | "architect", "deploy", "optimize" |
| **Forbidden vocabulary** | Terms that break voice | "easy", "simple", "game-changer" |
| **Competitor vocabulary** | Terms to avoid/reclaim | Varies by category |

---

## 4. Human-AI Collaborative Loop

The BVA workflow assumes a division of labor:

| Responsibility | Who |
|----------------|-----|
| Statistical synthesis (pattern detection, frequency, ASL) | AI |
| Strategic intent (cultural nuance, brand history, audience insight) | Human |
| Artifact generation (docs, prompts, style guides) | AI |
| Judgment calls on edge cases | Human |

**Iteration Protocol:**
1. Human provides corpus + business context
2. AI runs `/analyze` and returns metrics
3. Human validates metrics against brand instinct
4. AI runs `/synthesize` to produce voice pillars + system prompt
5. Human reviews and adjusts pillar definitions
6. AI generates platform pivots and prohibited/preferred lexicon
7. Human approves and deploys

---

## 5. Scoring Rubric

Use this rubric when running `/audit [output]` against the established voice:

| Dimension | Weight | How to Score |
|-----------|--------|--------------|
| Pillar adherence | 30% | Does each sentence reinforce ≥1 pillar? |
| Lexical compliance | 25% | Are prohibited words absent? Preferred words present? |
| ASL accuracy | 20% | Is avg sentence length within ±15% of target? |
| Cadence variance | 15% | Is σ within ±20% of target? |
| Sentiment temperature | 10% | Is emotional warmth within ±0.1 of target? |

**Total score 0–100.** Above 80 = on-brand. 60–80 = revision needed. Below 60 = fundamental voice break.

---

## 6. This-Not-That Logic Gates

The most actionable output of a BVA engagement. Each pillar should have 3–5 logic gates.

**Format:**
```
Pillar: [Name]
✓ USE: [Preferred expression]
✗ AVOID: [Prohibited expression]
WHY: [One-line rationale]
```

**Example — Pillar: Clinical**
```
✓ USE: "The system processes 10,000 requests per second under load."
✗ AVOID: "Our platform is blazing fast!"
WHY: Quantification replaces superlative. Claims must be reproducible.

✓ USE: "We recommend evaluating three alternatives before selecting."
✗ AVOID: "Obviously, this is the best choice."
WHY: Authoritative brands advise; they do not assert superiority.
```

**Failure modes to document:**
- Pillar collapse (voice loses all character under pressure)
- Overcorrection (clinical becomes robotic, witty becomes unprofessional)
- Platform bleed (LinkedIn tone bleeding into technical docs)
