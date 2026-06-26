---
name: artifact-deck
description: Public OpenClaw skill for generating reproducible PPTX decks from project notes, status bullets, and screenshots. Use when the user wants a stakeholder-ready deck from repo notes, release summaries, audit outputs, or screenshot evidence, and the deliverable should be a rebuildable `.pptx` rather than a freeform narrative.
version: 1.0.6
homepage: https://github.com/zack-dev-cm/artifact-deck
license: MIT-0
user-invocable: true
metadata: {"openclaw":{"homepage":"https://github.com/zack-dev-cm/artifact-deck","skillKey":"artifact-deck","requires":{"anyBins":["python3","python"]}}}
---

# Artifact Deck

## Goal

Turn curated project notes and screenshots into a clean, reproducible `.pptx` deck:

- one manifest that defines the deck title, subtitle, status slides, and optional appendix images
- one input check before build
- one local PPTX build
- one share-safe markdown summary with a rebuild command template and slide list

This skill is for deterministic stakeholder packaging, not autonomous research or design generation.
It requires Python 3.9+ and `python-pptx`.

## Use This Skill When

- release notes, weekly updates, or launch artifacts need to become a decision-ready deck
- browser screenshots or diagrams should be included as appendix slides
- the user wants a rebuildable `.pptx` instead of a one-off manual slide edit
- you need a concise executive or client status deck from repo-local notes

## Quick Start

1. Initialize the manifest.
   - Ensure the active Python environment already has `python-pptx` available.
   - Use `python3 {baseDir}/scripts/init_artifact_deck_manifest.py --title <title> --subtitle <subtitle> --section "What Changed=/abs/path/changes.md" --out <manifest.json>`.
   - Repeat `--section` for more markdown-backed status slides.
   - Optional: repeat `--slide "Risks=Pending scan|Need approval"` for direct bullet slides.
   - Optional: repeat `--image "Browser Proof=/abs/path/screenshot.png|Upload flow after publish"` for appendix slides.

2. Validate the inputs.
   - Use `python3 {baseDir}/scripts/check_artifact_deck_inputs.py --manifest <manifest.json> --out <check.json>`.
   - Fix missing content or image-path errors before building.

3. Build the deck.
   - Use `python3 {baseDir}/scripts/build_artifact_deck.py --manifest <manifest.json> --deck-out <deck.pptx> --out <build.json>`.
   - This writes the `.pptx` and a small JSON build summary.

4. Render the summary.
   - Use `python3 {baseDir}/scripts/render_artifact_deck_summary.py --manifest <manifest.json> --check <check.json> --build <build.json> --out <summary.md>`.
   - Share the deck and the summary together; the summary omits absolute local paths and keeps only a rebuild command template.

## Operating Rules

### Scope rules

- Keep the promise narrow: curated notes and screenshots in, reproducible `.pptx` out.
- Prefer concise bullets. Six bullets per slide is a practical ceiling.
- Treat missing or mistyped file paths as hard failures.

### Deck rules

- Use a title slide plus focused status slides.
- Put screenshots and diagrams in appendix slides unless the user explicitly wants them inline.
- Keep slide titles explicit: `What Changed`, `Risks`, `Asks`, `Appendix`, or equivalent.

## Bundled Scripts

- `scripts/init_artifact_deck_manifest.py`
  - Build a manifest from markdown sections, direct bullet slides, and optional image appendix entries.
- `scripts/check_artifact_deck_inputs.py`
  - Validate manifest structure, bullet availability, and image paths.
- `scripts/build_artifact_deck.py`
  - Generate the `.pptx` and a machine-readable build summary.
- `scripts/render_artifact_deck_summary.py`
  - Render a concise markdown summary with the deck filename, slide count, and a rebuild command template.
