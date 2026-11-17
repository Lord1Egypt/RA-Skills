---
name: douyin-tech-content-planner
description: Turn a technology or AI-tool topic and its source-backed facts into a focused Douyin video or image-post plan, with a clear audience, hook, evidence order, and optional call to action.
license: MIT-0
metadata:
  version: "1.0.0"
---

# Douyin Tech Content Planner

Use this skill to plan a short video or image post about technology, AI tools, software, or a ranked list. Work from the materials provided for this task. Do not assume a private workspace, repository, account, or platform policy file exists.

## Gather inputs

Use the topic, intended audience, format, target length if known, and the user's desired action. Identify factual claims and their sources. If a dynamic or consequential claim lacks a source, mark it unverified and either omit it or make it an explicit open question; do not turn it into a confident hook.

## Produce a plan

Create one focused plan containing:

- primary audience and one core search phrase;
- one specific viewer benefit;
- an opening hook that names the subject and gives a reason to continue;
- an opening sequence that brings a result, demonstration, or supporting evidence early;
- an ordered sequence of beats, each linked to the fact IDs it uses;
- a title direction and a reason the target audience might share the piece;
- at most one natural call to action, or `null` if none fits;
- uncertainties and omitted claims.

For video, use the first 0–3 seconds for subject and value, then make the opening evidence concrete within the first 12 seconds when the source material supports it. Do not force a fixed duration or invent a result to fill time. For image posts, adapt the same argument into pages and label the page sequence clearly.

Keep the project name, keywords, figures, and conclusions consistent across the title, hook, narration, captions, and post copy. Keep internal research notes out of audience-facing text. Do not add a disclaimer page, a station-exit instruction, or a call to action unless the subject or user request calls for it.

## Evidence contract

Give each source-backed input fact a stable `id`, source, and status. Only use facts marked `verified` in factual beats. Cite those IDs in the plan. Keep unverified or conflicting material in `unknowns`; explain what source or decision would resolve it. The included validator checks references and required structure, but cannot determine whether a source is credible or whether a claim is faithfully summarized. The AI must review the source content itself.

Use the JSON form in `README.md` with `scripts/validate_plan.py`. See `examples/` for a clearly hypothetical sample; do not repeat its contents as real product claims.
