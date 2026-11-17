# Fixture 17 — Without-skill baseline (BLE SoC comparison)

**Purpose**: Demonstrate the structural quality difference between an
LLM response generated *without* the embedded-solution skill loaded,
vs. the same query answered *with* the skill loaded (Top-3 comparison
table, Tier 1/2/3 citations, "not verified" markers, no fabrication).

This fixture is a **negative control**. The expected output is NOT what
the skill should produce — it's what a generic LLM produces when the
skill is *not* loaded. Use it as a baseline to measure how much the
skill improves over the default model behavior.

**User persona**: Engineer asking a simple question without engineering
specifics.

## Input prompt (verbatim)

> Without using the skill of embedded-solution, make comparison table for popular BLE devices

## What a generic LLM (no skill) typically produces

See `expected-outputs/17-without-skill-baseline.expected.md` for the
canonical baseline answer. Common failure modes the baseline exhibits:

1. **Fabricated BLE version numbers** — model claims "nRF5340 is BLE
   5.4" when Nordic's official spec is BLE 5.2 / 5.3 (depending on
   firmware revision). Training-data memorization confuses "newest nRF"
   with "newest BLE version".
2. **Single-point recommendation without comparison** — many LLMs
   default to "Top 1 + rationale" rather than the Top-3 + comparison
   table that the skill enforces.
3. **No tier / source citation** — every cell is presented as fact with
   no anchor to a datasheet URL, vendor page, or verification date.
4. **Missing the actual newest part** — TI CC2340R5 (real BLE 5.4 SoC,
   released 2024) is often absent from the candidate list because it
   post-dates much of the model's training cutoff for BLE SoC info.
5. **Inflated confidence** — every cell of the comparison table is
   filled, even where the model genuinely doesn't know. There is no
   "not verified" marker or honest "I don't know" admission.
6. **Conflated specs** — application-core flash and network-core flash
   are summed without explanation; external PSRAM is reported as
   "flash" without flagging it as optional / external.

## Why this fixture exists

The skill's value proposition is not "the skill knows more about BLE
SoCs than an LLM" — the model does have a lot of BLE knowledge. The
skill's value is **structural constraints** that:

- Force Top-3 + comparison table (Step 6)
- Force per-cell citation to a tier + URL + date (Step 6 + Step 7)
- Force "not verified" markers when data is missing (anti-pattern list)
- Force the catalog to be scanned (Tier 1 YAML first) so newly-released
  parts (like CC2340R5) are visible
- Force defaults-first so the model doesn't open with 5 questions

These constraints turn a confident-sounding but partly-fabricated
answer into a verified, source-anchored answer with explicit gaps.

## Acceptance criteria for the WITH-SKILL answer

The with-skill answer to the same prompt must:

- [ ] Give a Top 3 (not Top 1) comparison
- [ ] Include CC2340R5 as one of the candidates (it's the only true
      BLE 5.4 SoC in the catalog as of v0.3.0)
- [ ] Cite each cell with tier + URL + verification date
- [ ] Mark "not verified" cells explicitly instead of guessing
- [ ] Not inflate or conflate specs (application-core vs network-core,
      internal vs external flash)
- [ ] Have a self-audit "anti-patterns check" section listing what the
      response did NOT do

## Test methodology

To run this fixture as a comparison:

1. Ask the same prompt to the model **without** loading the
   embedded-solution skill. Save the response.
2. Ask the same prompt to the model **with** the embedded-solution
   skill loaded (skill installed via clawhub or unpacked into
   `~/.openclaw/skills/`).
3. Compare the two responses against the rubric in
   `evaluation-rubric.md` and the structural requirements above.

The without-skill response should score ≤ 10/25 on the rubric
(fabricated data, no citations, no "not verified" markers). The
with-skill response should score ≥ 20/25.

## Maintenance

This fixture should be re-run whenever:
- The skill adds new BLE SoC parts to the catalog (verify the
  without-skill response still misses them)
- The evaluation rubric changes axes / weights
- A new vendor releases a BLE SoC that should appear in the baseline

The without-skill baseline captured here is from 2026-06-28 using a
representative modern LLM with no domain-specific training between the
training cutoff and that date. Newer LLMs may score higher due to
knowledge updates, but the structural failures (no Tier 1/2/3 system,
no defaults-first, no anti-patterns) should persist.