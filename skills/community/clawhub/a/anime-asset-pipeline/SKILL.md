---
name: anime-asset-pipeline
description: Pipeline for producing anime/2D character art with an AI image model, focused on identity locking, per-region defect checking, and 8-bit quantization budget. Use when generating or iterating on anime character art, sprite sheets, key visuals, MV frames, or any task where the same character must stay recognisable across many images. Covers anchor-image workflows, failure modes that cost real credits, and when parameter tweaks are provably invisible.
license: MIT
metadata:
  author: CatsMansion
  version: "0.1.0"
  origin: distilled from a 1372-sprite desktop-pet project and an anime MV production
---

# Anime asset pipeline

You are producing anime/2D character art for a project where the **same character must stay recognisable across many images**. This skill exists because the default way of doing this wastes credits and silently fails.

Read this whole file before generating anything.

## The four iron rules

These override your default instincts. All four were paid for with wasted renders.

### 1. Fix the picture layer, not the parameter layer

When the complaint is about **how something looks**, the fix belongs to the picture layer:

- composition, camera, depth of field, lighting, colour grading
- subtitle/typography system, event density, transition *treatment*

It does **not** belong to the parameter layer. Nudging a decay constant, a peak multiplier, or a window size is not a fix for a look problem.

**Before any change, ask: will this be visible in the finished image?** If no, do not make it.

### 2. Criteria prove "done correctly", never "looks good"

A checklist going all green is not evidence of quality. Criteria catch mechanical errors — missing frames, broken loops, wrong regions touched. They say nothing about whether the result is any good.

Never present a green checklist as proof that the art is acceptable. Visual approval is a separate step and belongs to the human.

### 3. One comparison frame before any full re-render

Never re-render the whole batch to evaluate a tweak. Produce **one frame or one short segment** as an A/B, get it looked at, then re-render only after it passes.

Full re-renders to validate a small change are the single largest source of wasted spend in this workflow.

### 4. Stay inside the marked region

When asked to fix a region, touch only that region. Do not expand the scope, do not "improve" neighbouring areas, do not silently fix things that were not reported.

## When a change is provably invisible

On 8-bit material, the quantisation step is `1/base`:

| base | step |
|---|---|
| 200 | 0.005 |
| 220 | 0.0045 |
| 240 | 0.00417 |

Consequences, measured not guessed:

- a decay constant of 5 vs 6 differs by roughly **one quantisation level** — indistinguishable
- raising a peak from 1.03 to 1.06 moves the result by **one or two levels**

**Micro-tuning parameters on 8-bit source cannot produce a visible difference.** If you find yourself justifying a change by saying the numbers moved, stop.

See [references/8bit-budget.md](references/8bit-budget.md) for the arithmetic and the decision rule.

## The pipeline

### Stage 1 — Lock the character

Do not start from a text prompt. Text-to-image cannot hold a character's identity reliably across images.

1. Pick or produce **anchor images** — canonical views of the character (front, three-quarter, and whatever views the project needs).
2. Derive every subsequent image **image-to-image from an anchor**, never from text alone.
3. Verify the result against the anchor **feature by feature**, against real reference images. Not "it looks like her" — check each named feature.

See [references/identity-lock.md](references/identity-lock.md).

### Stage 2 — Generate

Standard practice, with two hard preconditions:

- **Check the channel before you start.** Model availability is per-session and changes. Probe it, and if it is not available, stop and report the blocker. Do not quietly switch to a different channel.
- **Check the balance before you start.** Know what the run costs before it runs.

### Stage 3 — Check per region

Go through the image region by region and look at each one. Naming the region is what makes the defect findable.

Known failure modes worth checking explicitly:

- **Local colour treatments do not lock.** A model that holds the overall character can still fail to hold a specific local colour feature. Three attempts at the same local feature is enough evidence — stop and change approach rather than retrying the same thing.
- **Frame-to-frame transitions in animation.** Look specifically at where a motion changes phase; that is where a missing intermediate frame hides.
- **Loop seams** if the asset loops.

See [references/defect-checklist.md](references/defect-checklist.md).

### Stage 4 — Reuse is free, sameness is not

Assets are not rationed. Reusing an image, an effect, or a transition as many times as the cut needs is normal and expected. Never add a usage cap or grey out "already used" options unless explicitly asked to prevent repetition.

If a sequence feels monotonous, the cause is almost always that **every section varies the picture the same way**. The fix is to vary the treatment — crop, mirror, composite mode, parallax — not to swap in different source images or rotate through a pool.

"Transition X appears twice" is not itself evidence of monotony. Diagnosing it as such is a wrong attribution.

### Stage 5 — Report

Order the report **failures first, then passes**. Then state explicitly:

- limitations
- any overspend
- anything not verified
- anything blocked by a missing dependency

If blocked, write the report anyway, including when nothing was started.

Template: [assets/review-report-template.md](assets/review-report-template.md).

## Channel discipline

- A channel being listed in your tool list does not mean it is callable. Definitions can be present while the channel is not mounted. Verify by actually calling it.
- Availability is per-session. A channel that worked yesterday may not be mounted today. Re-probe every session; never carry yesterday's result forward.
- If the required channel is unavailable: **stop and report.** Do not route around it via a different provider.
- If the human has banned a channel, it stays banned. Do not reach for it as a fallback.

See [references/channel-preflight.md](references/channel-preflight.md).

## Common misdiagnoses

| Wrong read | Correct read |
|---|---|
| "The checklist is green, so it looks good" | Criteria only prove mechanical correctness |
| "The chorus looks flat — tune the envelope" | Flatness is a picture-layer problem |
| "Transition X appears twice, that's repetitive" | Repetition comes from uniform variation, not reuse count |
| "We've used that image already, pick another" | Reuse is not rationed |
| "The numbers moved, so the output changed" | On 8-bit, one or two levels is invisible |

## Scope

This skill covers process discipline for 2D character art production. It does not cover model-specific prompt syntax, and it deliberately avoids naming specific providers — those change, and the discipline above does not.
