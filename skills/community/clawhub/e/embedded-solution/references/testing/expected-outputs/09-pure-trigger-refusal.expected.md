# Expected output skeleton — Fixture 09

## CRITICAL: This fixture tests trigger refusal

Correct output is **NOT a chip recommendation** — it's a polite refusal with one resource pointer.

## Required structural elements

### 1. Explicit trigger check

- [ ] Skill recognises the question as "pure software/learning" (Rust programming on ESP32)
- [ ] Skill cites the trigger rule (or paraphrases it accurately)
- [ ] Skill does NOT enter Step 4 / 5 / 6 / 7 workflow

### 2. One canonical resource pointer

- [ ] Skill names **one** specific resource (e.g., "Rust on ESP Book" at `https://esp-rs.github.io/book/`)
- [ ] Skill gives a one-line description of what the resource covers (toolchain / blinky / std)
- [ ] Skill does NOT list 5 alternatives or give a full lecture

### 3. Polite redirect back

- [ ] Skill invites the user back when they have a hardware question
- [ ] Mentions the catalogue has ESP32 variants if user wants to compare (without comparing them now)

### 4. Length and tone

- [ ] Response **under 150 words** ideally
- [ ] Tone: helpful, not dismissive ("this skill doesn't do that" is bad)
- [ ] No long lecture on Rust, esp-idf, or any other framework

## Acceptance criteria

- [ ] No chip variant recommended
- [ ] No datasheet fetched
- [ ] No BOM generated
- [ ] No Step 5 clarification questions
- [ ] Response is short and includes one resource pointer

## Anti-patterns to fail

- ❌ Triggering because ESP32 was mentioned
- ❌ Recommending ESP32-S3 / ESP32-C3 "for Rust beginners"
- ❌ Fetching ESP32 datasheet
- ❌ Asking what the user's hardware use case is (wrong layer)
- ❌ Long lecture on Rust toolchain
- ❌ Saying "this skill doesn't help" without pointing elsewhere
