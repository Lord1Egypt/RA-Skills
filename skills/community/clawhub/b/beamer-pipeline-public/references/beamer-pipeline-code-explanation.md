# Beamer Pipeline Public Architecture Notes

This document summarizes the reusable public subset of the Beamer pipeline. It intentionally omits private Telegram queue, launchd worker, OpenClaw session, local user path, and historical task-cache details from the upstream implementation.

## Public package scope

The public skill is centered on a local-first Beamer conversion contract:

1. Prepare local source assets.
2. Generate or guide generation of `analysis.json`.
3. Generate or guide generation of `slides.json`.
4. Generate `main.tex`.
5. Compile `main.tex` to `main.pdf` when a LaTeX toolchain is available.
6. Validate structured final acceptance fields.

## Included public files

- `SKILL.md`: skill-facing usage, inputs, outputs, and privacy notes.
- `templates/beamer_contract.md`: reusable Beamer generation contract.
- `scripts/run_beamer_public.js`: minimal public CLI wrapper.
- `scripts/prepare_task_assets.js`: markdown image localization and `asset_manifest.json` writer.
- `scripts/beamer_acceptance_contract.js`: structured final acceptance-field validator.
- `scripts/deck_symbol_canonicalization.js`: symbol canonicalization helper.
- `scripts/slide_schema.js`: slide/equation block normalization helper.

## Public call chain

```text
node scripts/run_beamer_public.js --input <source.md> --out <output-dir>
  -> scripts/prepare_task_assets.js <source.md> <output-dir> --mode beamer
  -> templates/beamer_contract.md copied into <output-dir>/beamer_task_contract.md
  -> downstream OpenClaw/agent generation uses that contract
  -> final output directory contains analysis.json, slides.json, main.tex, main.pdf, README.md, asset_manifest.json, figures/
```

## Artifact contract

A successful Beamer package should place every generated artifact in one canonical output directory:

- `analysis.json`
- `slides.json`
- `main.tex`
- `main.pdf` when compilation succeeds
- `README.md`
- `asset_manifest.json`
- `figures/`

Generated artifacts should not be split across historical fallback directories.

## Validation contract

The final response or machine-readable final report should expose these structured fields:

- `compile_status`
- `readability_status`
- `tex_warnings`
- `layout_policy`
- `visible_prose_recovery_hint`
- `visible_prose_fidelity_final`
- `render_fidelity_safeguards`

These fields are checked by `scripts/beamer_acceptance_contract.js`.

## Explicit exclusions

The public package does not include the private upstream runtime layers:

- messaging/slash-command adapters
- task queue database
- progress notifier
- long-running worker launcher
- local agent session recovery
- local machine paths
- private logs, caches, PDFs, and generated decks

The upstream reference snapshots, if present during local development, are excluded from publication by `.skillignore` and require manual review before sharing.
