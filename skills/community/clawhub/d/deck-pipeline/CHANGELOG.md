# Changelog

All notable changes are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

## [0.1.0] — 2026-05-12

### Added
- Initial public release.
- 4-stage pipeline: Sense Pass → McKinsey Translation → Layout Audit → Handoff.
- Polish-only mode for single-language decks (skips translation).
- Swappable `PROFILE` block (palette, fonts, glossary, style rules, slide-offset config).
- 10 helper scripts:
  - `sense_pass.py` — reverse-engineer design DNA (palette, fonts, size hierarchy).
  - `extract.py` — paragraph-level text extraction.
  - `apply.py` — apply EN edits + write comparison Excel.
  - `layout_audit.py` — font pollution cleanup + font-name suffix audit.
  - `overflow_recheck.py` — overflow estimator with HIGH/MED/LOW tiers.
  - `anchor_detect.py` — cross-page structural-anchor detection.
  - `glossary_audit.py` — late-stage glossary re-scan + wavering detection.
  - `excel_sync.py` — bidirectional PPT ↔ Excel sync, configurable CN↔EN slide alignment.
  - `handoff.py` — HANDOFF.md template writer.
  - `style_distill.py` — distill style fingerprint from a reference PDF/.pptx.
- Page-by-page execution with per-slide user checkpoint.
- Extensible style references (McKinsey baseline; users can layer additional reference samples).
- Bidirectional PPT ↔ Excel sync (ordinal-position + fuzzy fallback).
- Overflow estimator improvements: honors `auto_size`, reads real margins, per-character width by class, greedy word-wrap simulation.
- Font-name suffix audit (`Bold`/`Regular`/`Italic`/`Light` not allowed in `font.name`).
- Structural-anchor cross-page detection (auto per-page compression protection list).
- Discrete `-0.1pt` font compression step; line-spacing fallback (1.25 → 1.15).
- Companion-file lock detection (`~$xxx`).
- Excel three guard-rails (pre-write check, post-write readback, reverse sync).
- HANDOFF.md as a session-end deliverable.
- Bilingual README (English + 中文).

### Sources / credits
- The generic deck-globalization engine is derived from upstream
  **DeckGlobalizer v2.1.1** by tinadu-ai
  (<https://clawhub.ai/tinadu-ai/deckglobalizer>).
  Original three-phase architecture (Visual Audit / Semantic Alignment /
  Page-by-Page Execution) credited and retained.
