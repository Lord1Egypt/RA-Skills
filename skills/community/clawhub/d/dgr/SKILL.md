---
name: dgr
version: "1.1.0"
description: Superseded reference skill: structured reasoning records, kept for provenance. Enforcement moved to DGR Gate, a pre-execution gate for OpenClaw tool calls: clawhub.ai/dgr-ai-labs/plugins/openclaw-dgr-gate
homepage: https://www.clawhub.ai/sapenov/dgr
metadata:
  openclaw:
    emoji: "🧭"
  category: "reasoning"
---

> **Superseded — kept as a reference.** This skill formats reasoning into a structured record. It cannot stop an action; the model decides whether to follow it.
>
> **A rule in the prompt is a request. A rule in the tool is a gate.** The enforcing successor is [DGR Gate](https://clawhub.ai/dgr-ai-labs/plugins/openclaw-dgr-gate), a pre-execution gate that checks a call against operator-configured policy before it runs. It currently gates two demo tools, not your real ones.
>
> This page remains published as the record of the earlier approach and why it was replaced. Existing installs keep working; no further development.

# DGR — Decision‑Grade Reasoning (Governance Protocol)

**Purpose:** produce an auditable, machine‑validated decision record for review and storage.

**Slug:** dgr · **Version:** 1.1.0 · **Modes:** dgr_min / dgr_full / dgr_strict · **Output:** schema-valid JSON

## What this skill does
This skill produced a structured decision record: decision context, explicit assumptions, identified risks, a recommendation with rationale, and a consistency check. The output was documentation of reasoning, formatted as schema-valid JSON for easier review and storage.

That was insufficient. A model's own justification is not evidence — a better-formatted rationale from the same model does not change that. A prompt-level instruction can be lost during context compaction or ignored after the model reads untrusted text. This approach documented reasoning but could not enforce constraints on tool execution.

## What this skill is NOT (non‑claims)
This skill does **NOT** guarantee:
- correctness, optimality, or truth,
- elimination of hallucinations,
- legal/medical/financial advice suitability,
- or regulatory compliance by itself.

DGR improves **process quality** (clarity, traceability, reviewability) — not outcome certainty.

## When to use
Use when you need:
- an auditable record of reasoning,
- explicit assumptions/risks surfaced,
- reviewer‑friendly structure,
- a consistent output format across tasks and models.

## Inputs
- A user request/question (free text).
- Optional: context identifiers (ticket ID, policy name), and desired **mode**: `dgr_min`, `dgr_full`, or `dgr_strict`.

## Outputs
A single JSON artifact matching `schema.json`.

Minimum acceptance criteria (see `schema.json`):
- at least **1 assumption**
- at least **1 risk**
- `recommendation` present
- `consistency_check` present

## Safety / governance boundaries
- Always **ask for clarification** if key decision inputs are missing.
- If the decision is high‑risk, escalate via `recommendation.review_required = true`.
- If uncertainty is high, explicitly state uncertainty and limit scope.
- Do not fabricate sources or cite documents you did not see.

## Changelog
**1.1.0** — Repositioned as a superseded reference. Terminology aligned with DGR Gate (pre-execution gate). Removed usage guidance; this skill formats reasoning and does not enforce. Existing installs unaffected.

**1.0.4** — Remove redundant CLAWHUB_SUMMARY.md; summary now sourced from SKILL.md front-matter.

**1.0.3** — Tighten front-matter description for better conversion, add reasoning category, compress identity block for faster scanning.

**1.0.2** — Add ClawHub front-matter metadata with emoji and homepage for improved discovery and presentation.

**1.0.0** — Initial public release of DGR skill bundle with auditable decision reasoning framework, governance protocols, and structured output format.

> Note: This is an **opt‑in** reasoning mode. It is meant to be used alongside human decision‑making, not as a replacement.
