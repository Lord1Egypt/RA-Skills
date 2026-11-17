# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
in a lightweight, practical way.

## [Unreleased]

### Added

- `references/high-frequency-answers.md` for stable handling of common technique, rescue, and substitution questions.
- `references/dish-coverage.md` for practical mapping from common household ingredient bundles to high-success dishes.
- `references/sauces.md` for core home-cooking sauce profiles and ratio baselines.

### Changed

- Updated `SKILL.md` reference loading and capability priority order:
  1. high-frequency answers
  2. dish coverage
  3. sauces
- Added `Changelog` and `Releases` entry links to `README.md`.

## [0.2.0] - 2026-10-04

### Changed

- Rename `cooking-skill` to `brainharness-cooking` and align repository links and installation names with BrainHarness.
- Update distribution metadata and documentation; preserve skill behavior and historical release notes.

## [0.1.0] - 2026-04-08

### Added

- Initial `cooking.skill` core with routing for:
  - craving-based dish recommendation
  - ingredient-based dish recommendation
  - specific dish / technique questions
- Core reference docs:
  - `references/style-guide.md`
  - `references/cooking-framework.md`
  - `references/techniques.md`
- Multi-language README set:
  - Chinese
  - English
  - Japanese
  - Spanish
  - German
  - Korean
  - Portuguese
  - Russian
- MIT license
- Install guidance for:
  - `npx skills add`
  - `openclaw skills install`
  - manual `git clone`
- Distribution-facing example assets:
  - `examples/basic-flows.md`
  - `examples/demo-prompts.md`
- Lightweight evaluation anchor:
  - `evals/evals.json`

### Changed

- Localized README headers and titles were aligned for a more consistent repository presentation.
- Main README was expanded to better explain:
  - what the skill is
  - what it is not
  - what it is best at
  - where to find quick examples
- Local planning docs under `docs/` were removed from git tracking and added to ignore rules so they remain local-only.

### Notes

- `0.1.0` is the first public release tag for this repository.
- It represents the first installable and demoable snapshot, not the first internal draft.
