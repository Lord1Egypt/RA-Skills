# Reference-First Workflow (P0 upgrade, v2.5)

The 2026 industry baseline for character consistency is **reference-image-first**:
text anchors alone cannot guarantee pixel-level identity. This module upgrades the
template so reference images are a first-class citizen, with the anchor sentence as
the second layer of defense.

## Decision rule (run before generating)

1. Fix the **target model** for the job.
2. Look up its **reference-image method** in `ReferenceImageCapabilityMatrix.csv`.
3. Prepare the **reference pack** (quality gates below).
4. Assemble: reference pack + prompt assembled per `NaturalLanguagePromptTemplate.csv`.
5. If the model has NO strong reference method (DALL-E 3 tier), route to a
   conversational model or mark the job as description-only with verbatim anchors.

## Reference pack quality gates (all must pass)

| Gate | Standard |
|---|---|
| Resolution | ≥1024×1024, sharp focus, clean background |
| Lighting | Clear front-facing light on the identity reference |
| Angles | 2-3 images: front, 3/4, side (turnaround sheet = gold standard) |
| Style | Matches the target art style; avoid heavy makeup / extreme lighting |
| Version | The closer to the target version (outfit/hair), the better |

A **character turnaround sheet** (front + 3/4 + side + back composited into one
image) is the gold standard for identity anchoring.

## Per-model reference methods

| Model | Method | Strength knob | Notes |
|---|---|---|---|
| Midjourney / Niji | `--cref URL` + `--cw 0-100` | `--cw` up = stronger face, lower pose freedom | 80-100 portraits; 30-50 varied poses; pair `--sref` for style |
| SD 1.5/XL/3 | LoRA (trained) > IP-Adapter (no training) | LoRA trigger token | LoRA = gold standard for high-volume; IP-Adapter 80% of LoRA quality, 0% setup |
| Flux | Kontext (identity) / Redux (style/variant) | Reference image + prompt | Kontext keeps identity across scenes |
| GPT-4o / Gemini | Native reference upload | First image = anchor | Highest iteration efficiency: fix in conversation |
| DALL-E 3 | ❌ none | — | **Deprecated** — route to conversational model |
| Jimeng / Kling / Doubao / Tongyi | Partial, per official docs | Per vendor | Verify before integrating; treat as DALL-E 3 tier without strong refs |

## Two-layer defense (reference + anchors)

Reference images fight **identity drift**; verbatim anchor sentences fight
**attribute bleed** and **outfit drift**. Both layers are required for a series:
- Reference pack locks bone structure / face.
- Anchor sentences (verbatim) lock hair, mole, dress color, accessories.
- Never substitute synonyms in anchor sentences — models treat synonyms as
  different concepts.
