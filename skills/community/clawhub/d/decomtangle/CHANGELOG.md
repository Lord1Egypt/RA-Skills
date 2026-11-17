# Changelog

All notable changes to the `decomtangle` skill package. Format follows
[Keep a Changelog](https://keepachangelog.com/); versions follow SemVer.

## [Unreleased]

## [0.1.1] — 2026-07-06

### Changed

- Working defaults: new **minimal-arguments rule** — omit optional tool-call
  arguments entirely; emit booleans/numbers as bare JSON literals. Motivated by
  a live 2026-07-06 failure: an otherwise-atomic call was rejected by a strict
  tool-call parser because the model emitted `"background":"false"` (string
  instead of boolean), crashing the proxy layer. Fewer arguments = fewer
  type-error surfaces.

## [0.1.0] — 2026-07-06

### Added

- Initial `decomtangle` skill package:
  - `SKILL.md` — the five rules (atomic calls, step→observe→step, N steps =
    N calls, attempted ≠ confirmed, complexity tripwire) + working defaults
    (including atomic pacing between polls) and explicit is/is-not scope
    (in-loop tool-stepping discipline, NOT a goal/TODO planner).
  - `references/decomposition-heuristics.md` — observable-action /
    decision-point / failure-isolation tests, the quoting-depth tripwire
    (measured within the argument value; envelope excluded) with standard
    defusals (payload-to-file, split-the-pipeline, native endpoint), "when a
    single call IS enough" including rate-limited-surface pacing, and an
    anti-pattern catalog.
  - `references/atomic-call-checklist.md` — six-point per-call pre-flight
    (VERB / OBSERVE / FLOW / QUOTE / CONSUME / LOCAL) + milestone-reporting
    rule (procedures never end silently).
  - `examples/bad-mega-script-stall.md` — a real 2026-07-04 production
    incident, annotated layer by layer (mega-call → unparseable emission →
    gateway parser error → proxy `KeyError: 'message'` HTTP 500 → turn death
    with no terminal event).
  - `examples/good-multicalendar-atomic.md` — the same virtualized-calendar
    procedure completed as ~18 atomic calls on the same model: bounded poll
    reads, the Rule-5 payload-to-file pattern, and a fresh-load verification
    leg that is itself a multi-call procedure.
  - `SKILL_CARD.md` (NVIDIA trust format), `README.md`, `LICENSE` (MIT),
    `CLAWHUB.md` (listing copy).
