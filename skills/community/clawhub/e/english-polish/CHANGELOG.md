# Changelog

## 1.0.0 — 2026-06-19

First stable release of the english-polish skill.

### Added
- **19-class pattern library** (A–S) for Chinglish detection:
  - A–L: original patterns (subject dangling, passive stacking, noun stacking, etc.)
  - M–S: new Chinese-logic patterns (emphasis inversion, list cadence, concessive clusters, topic-comment fronting, false inclusive "We", logical sawtooth, list summarizer)
- **Three-phase polish pipeline**:
  - Phase 1: Grammar & mechanics (articles, prepositions, subject-verb agreement, comma splices)
  - Phase 2: Chinglish pattern replacement (19 categories of direct translation fixes)
  - Phase 3: Style & idiom (connector diversification, "There is/are" → direct, passive→active, long sentence breakup, unnecessary "that" removal)
- **Config system** (`config/`): `default.json` built-in config, optional `user.json` for custom patterns and replacement rules
- **Makefile CI targets**: `make test`, `make baseline`, `make save-baseline`, `make check`, `make clean`
- **Baseline regression tracking**: auto-saves and compares full-book average score for regression detection (±0.1 threshold)
- **Full test suite**: 29 test cases (19 pattern tests + 5 clean text + 5 boundary cases), 28/29 passing

### Fixed
- P2 sentence boundary protection: auto-capitalization after deletions, double-space cleanup, leading comma removal
- Diff output: from hard 2,000-char truncation to intelligent 80-line cap with total summary
- Phase 3: from empty shell ("manual review needed") to 6 sub-operations
- `KeyError: 'score'` in detector.py (#284)
- F_noun_stacking false positives tightened
- M_emphasis_inversion multi-word X support
- L_weak_verb past-tense support

### Performance
- Full-book baseline (19 chapters + 13 support files): 4.89/5 average
- All 32 files at Native-level (≥4.5)
- 294 total detections across 19 categories

## 0.x — Pre-release

Internal development versions (unpublished).
