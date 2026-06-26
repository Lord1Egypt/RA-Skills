---
name: brand-voice-architect
description: >
  A high-precision engine for deconstructing, documenting, and synthesizing brand-specific
  linguistic patterns and tonal architectures. Use this skill whenever a user wants to:
  create or generate a brand voice guide, analyze writing samples or a corpus for tone/style,
  review content for linguistic consistency, build a voice system prompt, define brand pillars,
  identify prohibited words or preferred vocabulary, create "this not that" style guides,
  adapt tone across platforms (LinkedIn vs. technical docs vs. social), or reverse-engineer
  competitor or reference brand voices. Trigger even for loosely related requests like
  "make our writing more consistent", "what tone should we use?", or "analyze how we write."
---

# Brand Voice Architect (BVA)

A skill for engineering, documenting, and synthesizing brand-specific voice with quantifiable precision. Brand voice is treated as a **Linguistic DNA** — a measurable baseline, not an aesthetic preference.

---

## Core Workflow

### Phase I: Decomposition — `/analyze [corpus]`
Run a linguistic audit on provided text samples:
1. **Lexical Audit** — High-frequency verbs/adjectives, prohibited terms, vocabulary signature
2. **Structural Mapping** — Average Sentence Length (ASL), syntactic complexity, variance
3. **Sentiment Baseline** — Emotional temperature on a 0.0–1.0 scale

→ Use `scripts/voice_analyzer.py` to compute metrics programmatically when a corpus is provided.

### Phase II: Architectural Design — `/synthesize [pillars]`
Build the voice matrix:
1. **Pillar Definition** — Establish 3 core attributes (e.g., *Authoritative, Wit-driven, Technical*)
2. **The Spectrum** — Define "This, Not That" logic gates for each pillar
3. **Persona Encoding** — Translate pillars into LLM system-level instructions

→ Use `scripts/prompt_synthesizer.py` to generate deployable system prompts.

### Phase III: Delivery
1. **Artifact Generation** — Produce voice guide docs, style reference cards, prompt templates
2. **Manual Review** — `/review [output]` provides a qualitative checklist to assess whether output aligns with the established voice pillars (Claude-assisted, not script-automated)
3. **Platform Pivot** — `/pivot [context]` adapts voice for specific channels while preserving DNA, using `generate_platform_pivot()` from `prompt_synthesizer.py`

> **Note on prohibited words:** The generated system prompt instructs the LLM to replace prohibited words with preferred equivalents. This is a prompt-level instruction — enforcement depends on the model following the system prompt, not on automated script-level filtering.

---

## The 4-Pillar Framework

Map every brand voice across four axes to define its **Safe Operating Area**:

| Axis | Poles |
|------|-------|
| **Character** | Friendly ←→ Authoritative |
| **Tone** | Humorous ←→ Serious |
| **Language** | Simple ←→ Complex |
| **Purpose** | Helpful ←→ Entertaining |

See `references/methodology.md` for full framework details including Cadence Analysis and Semantic Salience scoring.

---

## Mandatory Output Components

Every Brand Voice engagement must produce:

1. **Metrics Report** — Lexical density %, ASL, top keywords, cadence variance
2. **Voice Matrix** — 3 pillars × "This/Not That" for each
3. **System Prompt** — Ready-to-deploy LLM persona encoding
4. **Platform Pivots** — At minimum: formal/informal, long-form/short-form variants
5. **Prohibited/Preferred Lexicon** — Concrete word lists

---

## Quick Reference Commands

| Command | Action | Implementation |
|---------|--------|---------------|
| `/analyze [corpus]` | Linguistic audit on provided text | `scripts/voice_analyzer.py` |
| `/synthesize [pillars]` | Generate LLM system prompt from pillars | `scripts/prompt_synthesizer.py` |
| `/review [output]` | Qualitative checklist review against voice pillars | Claude-assisted (no script) |
| `/pivot [context]` | Adapt voice for target platform/audience | `generate_platform_pivot()` in prompt_synthesizer |

---

## Scripts

- `scripts/voice_analyzer.py` — Computes lexical density, ASL, cadence variance, sentiment temperature, and top keywords from a corpus
- `scripts/prompt_synthesizer.py` — Generates deployable LLM system prompts from a `BrandConfig` object; includes `generate_platform_pivot()` for channel-specific adaptations

## References

- `references/methodology.md` — Full technical methodology: 4-Pillar Framework, Cadence Analysis, Semantic Salience, Human-AI Collaborative Loop
