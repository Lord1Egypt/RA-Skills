# Fixture 09 — Pure trigger refusal (Rust on ESP32)

**User persona:** Hobbyist programmer learning embedded Rust
**Source conversation:** 2026-06-27 (added after SKILL.md trigger rules clarified)

## Input prompt (verbatim)

> "How do I write a Hello World in Rust on the ESP32? I'm new to embedded programming."

## What the skill should do

1. **Trigger check** — this is the critical decision. The user mentions ESP32 (a chip in our catalogue) but the question is **purely software/learning**. SKILL.md explicitly lists this in "Do NOT trigger for":
   > "Pure software/learning questions (e.g., 'how to write Hello World in Rust on ESP32')"

2. **Skill MUST refuse to trigger** — but politely, with a useful redirect.

3. **What NOT to do**:
   - Don't recommend an ESP32 variant (ESP32-S3 vs ESP32-C3 vs original ESP32)
   - Don't fetch the ESP32 datasheet
   - Don't run Step 4 / 5 / 6 workflow
   - Don't generate a BOM
   - Don't enter Step 7 external lookup

4. **What TO do**:
   - Recognise the question is purely software / language / learning
   - State clearly: "This skill triggers for embedded system design (chip selection, BOM, datasheet parameters). It does NOT trigger for software/learning questions like Rust on ESP32."
   - Suggest the right resource (Rust on ESP book at `https://esp-rs.github.io/book/`, esp-rs std training, or ferrules/embassy frameworks)
   - Acknowledge the user might be interested in *which ESP32 variant* if their question evolves — invite them back when ready

## Expected behaviour (structure)

A short, friendly refusal with one pointer to the canonical Rust+ESP resource. NOT a long lecture on Rust or ESP-IDF.

### Example acceptable response

> This skill is for embedded system design (chip selection, BOM, datasheet parameters) — not Rust programming tutorials. For "Hello World on ESP32 with Rust", the canonical resource is the [**Rust on ESP Book**](https://esp-rs.github.io/book/) — covers toolchain setup, blinky, and standard library on ESP32 / ESP32-S3 / ESP32-C3.
>
> If your question evolves into "which ESP32 variant should I pick for my [product]" — come back and I'll help (we have ESP32-C3, ESP32-S3, ESP32-C6, and original ESP32 in the catalogue).

## Acceptance criteria

- [ ] Skill **does NOT enter Step 4/5/6/7** workflow
- [ ] Skill does NOT recommend any chip variant
- [ ] Skill does NOT fetch any datasheet
- [ ] Skill explicitly cites the trigger rule ("software/learning question, out of scope")
- [ ] Skill provides **one** canonical resource pointer (Rust on ESP book or similar)
- [ ] Skill invites user back when they have a hardware question (not too pushy)
- [ ] Response is **short** (under 150 words ideally) — no lecture

## Anti-patterns to fail

- ❌ Triggering anyway because "ESP32" was mentioned
- ❌ Recommending ESP32-S3 over ESP32-C3 "for Rust beginners" without being asked
- ❌ Fetching ESP32 datasheet to compare variants
- ❌ Running Step 5 ("what's your application?") — wrong layer entirely
- ❌ Long lecture on Rust toolchain, esp-idf vs esp-rs, etc.
- ❌ Saying "this skill doesn't help with that" without pointing to where it can help
- ❌ Generating a BOM for "ESP32 dev board + breadboard + LEDs" (out of scope)

## How this fixture complements the suite

Fixture 02 (student BLE learning) tests **valid trigger** (chip selection with educational angle). Fixture 09 tests **invalid trigger** (pure software). Together they pin down the boundary of the trigger rule.
