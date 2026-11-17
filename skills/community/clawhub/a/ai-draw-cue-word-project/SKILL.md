---
name: ai-draw-cue-word-project
slug: ai-draw-cue-word-project
displayName: AI Drawing Prompt Engineering Expert
description: Build high-consistency AI character prompts across five model syntax families (natural-language / conversational / MJ-Niji / SD / domestic API) and multi-format outputs (image / storyboard / comic panel / video / 3D) using a weight & ratio precision-control workbench. Ships character-anchor sheets, composition & shots references, posture-emotion mapping, reference-image capability matrix, multi-character spatial relations, an orientation token bank with OR-01…OR-08 screen-direction rules, storyboard/panel layout rules, speech-bubble positioning, LoRA management, temporal-consistency checklist, 3D generation matrix, video prompt template, conversational edit chain, negative-word bank, and a P0/P1/P2 validation checklist. All example characters in this skill are adult (18+) women; no minors allowed.
version: 3.0.0
metadata:
  openclaw:
    requires: {}
    homepage: "https://github.com/nohn3043-arch/ai-draw-cue-word-project"
---

# AI Drawing Composition Template (ai-draw-cue-word-project)

A quality-control workbench for generating character prompts that stay consistent
across models and across a series of images. The setting layer (anchors, composition,
validation) is model-agnostic; the syntax layer is adapted per model family.

## Safety & Content Policy (read before use)

- **No sexualization of minors.** Never generate, refine, or optimize imagery that sexualizes, eroticizes, or exploits anyone depicted as a minor or under 18. This applies to every model family and every syntax flow in this skill.
- **Adult characters by default.** All example characters in this skill (including Nanwang and Song Jiuning) are depicted as **adult women (18+)**. Do not reintroduce minor ages ("16-year-old", "teen girl", "loli", "少女", "未成年") into anchors, prompts, or logs.
- **No mixing of age stages.** A character version is either adult-only or absent; never use cross-stage head-to-body ratios, childlike features, school uniforms, or any other visual cues historically associated with minors in adult-character anchors.
- **Per-version adult declaration.** Every new row added to `CharacterAnchors.csv` / `FeatureDetails.csv` / `NaturalLanguagePromptTemplate.csv` must include an "Adult (18+)" cell. Prompts missing this cell are invalid and must be regenerated.
- **User responsibility.** You are solely responsible for ensuring generated content complies with applicable laws and platform policies in your jurisdiction. This skill is a prompt-engineering workbench, not legal or safety clearance.
- **Fictional / non-sexual character design only.** The workbench is intended for fictional, non-sexual character-concept and illustration work. If you are unsure whether a request is appropriate, do not generate it.

### v2.9.0 safety-patch changelog (2026-09-01)

- Hardened Safety & Content Policy: added `No mixing of age stages` and `Per-version adult declaration` rules.
- All example characters explicitly declared as adult (18+) women.
- Old `SKILL.md.bak-20260829` soft-deleted to `.workbuddy/.trash/2026-09-01/`.

### v3.0.0 orientation-standard release (2026-11-06)

- **Two new sheets close the orientation gap.** Every prior sheet constrained *where* a character is; none constrained *which way they point*. `references/OrientationTokenBank.csv` is the vocabulary layer (19 legal tokens: facing 6 / motion_vector 9 / camera_side 4, each with an EN and ZH prompt phrase plus a counter-example); `references/OrientationAndScreenDirection.csv` is the rulebook layer (3 field definitions + 8 mechanical assertions OR-01…OR-08 + 2 control rules).
- **Token-or-nothing input.** Free-text orientation is invalid input anywhere in this standard — tokens exist so that a validator can compare them, and it cannot compare adjectives.
- **Checklist and rulebook agree.** 3 P0 rows appended to `TemporalConsistencyChecklist.csv` (Orientation: facing consistency / motion vector reversal / axis side) and 2 rows to `MultiCharacterSpatialRelations.csv` (Facing assignment / Motion vector chain).
- **CSV defect fixed.** Unquoted commas in `MultiCharacterSpatialRelations.csv` line 9 (Scale perspective) made that row parse as 8 columns.
- **Two Doubao examples added.** `examples/doubao_ai_girl_fanart_prompt.md` (AI娘图鉴 style) and `examples/doubao_character_sheet_prompt.md` (girl + mature versions).
- **The v2.9.0 / v2.9.3 adult-declaration safety patch is retained.** The upstream v3.0 sheets were re-checked; the skill keeps adult-only anchors and keeps the loli/teen baseline rows out of `AspectRatioBaselines`.
- Sheet count 21 → 23. Version: 2.9.3 → 3.0.0.

### v2.9.1 documentation release (2026-10-18)

- **Listing internationalized for ClawHub**: `displayName` changed from Chinese to English ("AI Drawing Prompt Engineering Expert"). The remaining Chinese strings are deliberate forbidden-token literals in the safety policy (`"少女"`, `"未成年"`) and stay verbatim so the guard keeps matching them.
- No behavioural change: the body was already English; only the display title and version changed.
- **v2.9.2 (2026-10-18)**: republished with the English display name bound at the registry level so the ClawHub listing title reads "AI Drawing Prompt Engineering Expert" instead of the slug. Content identical to 2.9.1.
- **v2.9.3 (2026-10-20) repository sync**: pulled the repo's v2.9 2026-10 model refresh into `references/` — MJ v8.2 / Niji v7 (`--oref`/`--ow` on v7, Edit Model on v8, `--cref`/`--cw` dead above v6, `::` weighting ended at v6.1), SD 3.5 / SDXL, FLUX.2 (no negative prompting), Gemini 3 Pro Image / Nano Banana Pro (5-part formula, numbered reference slots), Seedream 5.0 / domestic API. Updated `ModelsAndReferences`, `ReferenceImageCapabilityMatrix`, `NaturalLanguagePromptTemplate`, `VideoGenerationPromptTemplate`, `NegativeWordBank`, `NOTES.md` and the worked example; added `references/GLOSSARY.md`. **The v2.9.0 adult-declaration safety patch is retained** — the upstream refresh reverted the adult wording, so the skill keeps adult-only anchors, keeps the loli/teen baseline rows out of `AspectRatioBaselines`, and re-applies the adult declaration to the refreshed sheets and example.

## When to use

Use this skill when the user needs to generate or refine an AI image prompt for a
character — especially when consistency across multiple images or across different
models matters (illustrations, storyboards, character cards, series).

## Workflow (run through once per generation)

1. **Character anchors** — read `references/CharacterAnchors.csv`. Pick or create an
   image version row: identity anchor (≥1.6), temperament tag (≥1.3), palette,
   signature props, negative anchoring.
2. **Composition & shots** — read `references/CompositionAndShots.csv`. Fill the
   Section A config (aspect ratio, composition type, camera angle, shot scale, focal
   length, lighting, layers, occlusion). Choose composition type from the
   Composition Type Reference table in `references/NOTES.md` (Section B).
   Look up posture by temperament in the Posture-Emotion Mapping table
   (`references/NOTES.md` Section D) — never free-hand it.
2b. **Orientation** — read `references/OrientationTokenBank.csv` and
   `references/OrientationAndScreenDirection.csv`. Assign exactly ONE facing token
   per character per panel, plus a motion_vector and a camera_side note. Use literal
   tokens only (free-text orientation is invalid input); check OR-01…OR-08 before
   moving on. See `references/NOTES.md` (Orientation section) for the debugging order.
3. **Model & reference strategy** — read `references/ReferenceImageCapabilityMatrix.csv`
   to pick the model's consistency method (`--oref`/`--ow` on MJ v7, Edit Model on v8,
   LoRA, numbered reference slots, or verbatim anchor reuse for DALL-E 3). For series work, follow the
   **reference-first workflow** in `references/ReferenceFirstWorkflow.md` (P0).
4. **Assemble the prompt** — read `references/NaturalLanguagePromptTemplate.csv` for
   the syntax of the target family (see the five rows below).
5. **Validate** — run the P0/P1/P2 checks in `references/Checklist.csv`. Any P0
   failure (identity anchor, core features, anchor-description reuse, negative
   coverage) means regenerate. For sequences, also run OR-01…OR-08 from
   `references/OrientationAndScreenDirection.csv` — an orientation P0 fails the audit.
6. **Batch production** — for series / production runs, follow the pipeline in
   `references/ProductionPipeline.md` (P0): 12-image pre-flight, drift labels,
   retry rules, versioned reference pack.

## Five syntax families

| Family | Key rules |
|---|---|
| Natural language (FLUX.2 Pro / Max / Flex) | Full English paragraph: subject+action → style → context/lighting → camera. Front-load the non-negotiable anchor. Bind hex colors to specific objects; quote any must-render string. **No negative prompting** — rewrite affirmatively. |
| Conversational (Gemini 3 Pro Image / Nano Banana Pro, GPT-4o) | Google 5-part formula: subject / action / location / composition / style. Numbered reference slots (Image 1 = subject, Image 2 = pose), one sentence per role. One change + explicit preserve-list per edit; never re-describe a referenced face. |
| MJ v8.2 / Niji v7 | Core anchors in the first 20 tokens; CLI params appended at the end (`--ar`, `--oref`/`--ow` on v7, `--edit` on v8, `--s`, `--niji`). `--cref`/`--cw` are v6-only and dead above v6; `::` weighting ended at v6.1. Write `--niji 7` explicitly — Niji has no v8 counterpart. `--no` filters only 4-6 highest-risk words. |
| Stable Diffusion 3.5 / SDXL | Comma-separated tags: identity anchors (1.3-1.5) → core features → posture/composition → lighting (0.7-0.9). Use `(tag:weight)`; stay ≤1.5, >1.6 melts anatomy. Separate Negative Prompt box. |
| Domestic API (Seedream 5.0 / Jimeng / Kling / Doubao / Tongyi Wanxiang) | Chinese natural-language paragraph + API params (`aspect_ratio` / `size` / `force_single` / `seed`). Keep professional terms in their source language. Numbered refs with per-image roles. Negative-word support varies per vendor — follow official docs. |

## Weight semantics (SD/MJ numeric baseline)

| Weight | Meaning |
|---|---|
| 1.6-2.0 | Hard anchor — absolutely immutable, force-kept in every scene |
| 1.3-1.5 | Core feature — kept in all scenes, validated as P0 |
| 1.0-1.2 | Baseline — default strength, fluctuate ≤0.2 |
| 0.7-0.9 | Atmosphere — adjustable per scene |
| <0.7 | Weak prompt — atmosphere only, never carries key info |

Numeric weights are **SD-only**. MJ dropped `::` weighting at v6.1 (use token position instead); FLUX.2, Gemini 3 Pro Image and the domestic family have **no numeric weighting at all** — write emphasis into the sentence.

## v2.6–v3.0 multi-format outputs (image / storyboard / comic panel / video / 3D)

Beyond single-image generation, v2.6–v3.0 adds sheets for serialized and cross-modal work:

| Output | Key sheet | Rules |
|---|---|---|
| Multi-character scenes | `references/MultiCharacterSpatialRelations.csv` | Subject size hierarchy, occlusion, gaze direction, relative positioning anchors, facing assignment, motion vector chain |
| Comic panels / pages | `references/PanelLayoutRules.csv`, `references/SpeechBubblePositioning.csv` | Panel grid baselines (4-panel / 6-panel / cinematic strip / splash / vertical scroll), bubble placement by speech type (7 types) |
| Storyboard sequences | `references/StoryboardSkeletonTemplate.csv`, `references/TemporalConsistencyChecklist.csv` | Shot-to-shot continuity: 10 panel roles, 3 camera rules, 4 page layouts; 17 temporal checks across 7 categories |
| Orientation / screen direction | `references/OrientationTokenBank.csv`, `references/OrientationAndScreenDirection.csv` | 19 legal tokens (facing 6 / motion_vector 9 / camera_side 4) + OR-01…OR-08 mechanical assertions and 2 control rules |
| Conversational iterative editing (Gemini 3 Pro Image / GPT-4o) | `references/ConversationalEditChain.csv` | Single-point edits only, anchor sentences frozen, edit log structure |
| LoRA management | `references/LoRAManagement.csv` | Trigger tokens, weight baselines, version pins, conflict detection |
| Video generation | `references/VideoGenerationPromptTemplate.csv` | Motion verbs, camera trajectory, duration baselines per model family |
| 3D generation | `references/ThreeDGenerationMatrix.csv` | Model-specific syntax for 3D asset outputs (Turntable / orthographic / mesh) |

### v2.7 comic-mode edition
Added `PanelLayoutRules` (5 layout types), `SpeechBubblePositioning` (7 bubble types), and `TemporalConsistencyChecklist` (14 check items across 6 categories). Total sheet count 18→21.

### v2.8 comic-workflow closure
Interactive workbench deployed with bilingual (zh/en) comic mode workflow: storyboard skeleton → panel layout → speech bubble positioning → temporal consistency check. All 21 CSV sheets verified against deployed index.html data.

### v3.0 orientation-standard edition
Added `OrientationTokenBank` (19 legal tokens) and `OrientationAndScreenDirection` (3 field definitions + OR-01…OR-08 + 2 control rules); appended 3 P0 rows to `TemporalConsistencyChecklist` (Orientation category) and 2 rows to `MultiCharacterSpatialRelations` (Facing assignment / Motion vector chain); fixed the unquoted-comma CSV defect in `MultiCharacterSpatialRelations` line 9. Sheet count 21→23.

## Cross-model red lines

- `(word:1.3)` works only on SD; MJ uses token position; natural-language models
  forbid bracket weights.
- MJ `--no` ≤ 4-6 short words; SD has a Negative Prompt box; natural-language and
  domestic API models rely on affirmative writing first, negation as fallback.
- Anchor sentences must be reused verbatim — synonym rewriting breaks consistency.
- **DALL-E 3 is deprecated (v2.5)**: no reference-image support; for series or
  consistency-critical scenes, route to a conversational model (Gemini 3 Pro Image /
  GPT-4o) or a reference-capable natural-language model (FLUX.2) instead of
  compensating with description only.
- **Reference-first (v2.5)**: for any multi-image series, prepare a reference pack
  and follow `references/ReferenceFirstWorkflow.md`; text anchors are the second
  layer of defense, never the first.

## Files

- `references/*.csv` — the 23 workbench sheets (flat tables):
  - Core (v2.5 baseline): `CharacterAnchors`, `CompositionAndShots`, `AspectRatioBaselines`, `FeatureDetails`, `ModelsAndReferences`, `ReferenceImageCapabilityMatrix`, `NaturalLanguagePromptTemplate`, `NegativeWordBank`, `Checklist` (P0/P1/P2), `Usage`, `ChangeLog`, `GenerationIterationLog`
  - Multi-format (v2.6): `ConversationalEditChain`, `LoRAManagement`, `MultiCharacterSpatialRelations`, `PanelLayoutRules`, `SpeechBubblePositioning`, `StoryboardSkeletonTemplate`, `TemporalConsistencyChecklist`, `ThreeDGenerationMatrix`, `VideoGenerationPromptTemplate`
  - Orientation (v3.0): `OrientationAndScreenDirection`, `OrientationTokenBank`
- `references/NOTES.md` — supplementary tables & rules (composition types B,
  two-character interaction C, posture-emotion mapping D, weight semantics,
  narrative-intensity mapping, parameter interaction rules, strength ranking,
  orientation standard)
- `references/ReferenceFirstWorkflow.md` — P0 reference-first workflow (v2.5):
  decision rule, reference-pack quality gates, per-model methods, two-layer defense
- `references/ProductionPipeline.md` — P0 production pipeline (v2.5): 12-image
  pre-flight, drift labels, retry rules, versioned reference pack
- `examples/nanwang_spring_garden_prompt.md` — finished prompts in four syntax
  flows for the example character Nanwang
- `examples/doubao_ai_girl_fanart_prompt.md` — Doubao AI娘图鉴 style fan-art prompt
- `examples/doubao_character_sheet_prompt.md` — Doubao character-sheet prompts
  (girl + mature versions)

## Source

Version-controlled at github.com/nohn3043-arch/ai-draw-cue-word-project (also
SourceForge `p/ai-draw-cue-word-project` and Gitee `nohn-ecosystem/aidraw`).
Apache-2.0. Copyright (c) 2026 NOHN AI TECHNOLOGY PTE LTD.
