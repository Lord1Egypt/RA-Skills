# Lead Block Archetypes

Use these archetypes as drafting shapes.
Paraphrase them; do not paste them verbatim.

Compatibility note:
- the active compatibility-mode sentence defaults now live in `assets/lead_block_compatibility_defaults.json`
- update that asset when the issue is fallback cadence or reusable sentence wording, and update this file when the issue is the underlying chapter-lead method

## 1. Lens-first

Use when:
- the chapter brief already has a strong throughline
- the reader mainly needs the chapter's comparison lens up front

Move pattern:
- sentence 1: state the shared comparison problem
- sentence 2: name the recurring contrasts
- optional sentence 3: calibrate how evidence or protocol assumptions affect comparison

Example:
- `What matters most in this chapter is not whether the systems share a surface architecture, but which assumptions make their decisions comparable under the same evaluation setting.`

## 2. Contrast-first

Use when:
- the chapter is held together by 2-3 recurring trade-offs
- the H3 subsections are easy to over-read as isolated methods

Move pattern:
- sentence 1: introduce the recurring trade-off
- sentence 2: show how different subsections expose different sides of it
- sentence 3: state why that contrast matters for interpretation

Example:
- `The central contrast in this chapter is between flexibility and control: each subsection changes how much structure the system fixes in advance and how much it leaves to runtime adaptation.`

## 3. Calibration-first

Use when:
- the comparison only makes sense if the reader keeps protocol or evidence assumptions in view
- the chapter includes evaluation, reproducibility, or deployment constraints

Move pattern:
- sentence 1: state the high-level calibration rule
- sentence 2: connect that rule to the chapter's subsections
- sentence 3: preview the design choices that the chapter will compare under that rule

Example:
- `The comparisons in this chapter only hold if protocol assumptions stay visible, because the same design choice looks very different once budget, access, or observability changes.`

## 4. Problem-first

Use when:
- the chapter brief defines a shared bottleneck or failure surface
- the subsections are best read as different answers to the same question

Move pattern:
- sentence 1: name the bottleneck
- sentence 2: show how each subsection addresses it differently
- sentence 3: explain the comparison lens that keeps those answers on the same scale

Example:
- `This chapter is unified by a single bottleneck: once the system must act under limited feedback, design choices that seem local become coupled to evidence quality, cost, and stability.`
