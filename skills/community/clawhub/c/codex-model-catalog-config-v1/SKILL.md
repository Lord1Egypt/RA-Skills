---
name: codex-model-catalog-config
description: Manage models in the existing Codex model-catalogs/default.json catalog on Windows or macOS. Use when a user asks to add, modify, remove, or list models in that exact catalog. Do not use to install, repair, or reconfigure global Codex settings.
---

# Codex Model Catalog Config

Modify only the user's existing `default.json` catalog according to the explicit request. Treat the catalog as the source of truth.

Do not inspect or modify `config.toml`, even if it appears to be missing the catalog setting. Do not create or restore the catalog from the bundled asset during normal model management. Do not create a backup of the old catalog.

## Target File

Resolve the Codex home directory in this order:

- Use `CODEX_HOME` when it is set.
- On Windows, default to `%USERPROFILE%\.codex`.
- On macOS, default to `$HOME/.codex`.

The target is exactly:

`<CODEX_HOME>/model-catalogs/default.json`

If the target does not exist, stop and report that path. Do not search for another catalog or create a replacement elsewhere.

## Efficiency Rules

Each entry embeds very large `base_instructions` / `model_messages` strings. Never read or print the whole file into the response.

- Inspect with one compact probe that lists only `slug`, `context_window`, `max_context_window`, `default_reasoning_level`, and whether `tool_mode` is present. Do not echo `base_instructions` or `model_messages`.
- Do not read the raw file and then inspect it a second time. One probe answers both "does the slug already exist" and "which entry do I clone".
- Make the edit in memory and write once. Do not stage intermediate copies or temp files.
- Locate an entry by its `"slug"` line and the surrounding object braces; do not enumerate every field.
- Keep round trips minimal: one probe, then one write-and-validate step.

## Workflow

1. Run one compact probe to confirm the file exists, confirm a top-level `models` array, list the current slugs, and capture only the fields the request needs.
2. Follow the user's written request only. Do not add unrelated validation, repairs, settings changes, or files.
3. For an added model, ask only for model-specific values that the user omitted. Clone a compatible existing entry when one is available, then change only the requested fields. Reject a duplicate slug.
4. Do not add `tool_mode` to a new entry. If the chosen source entry has `tool_mode`, remove it from the new entry even though the source model remains unchanged.
5. For a modified model, require an exact existing slug and change only the requested fields. Preserve every other model and field.
6. For a deleted model, remove only the explicitly named entry. Otherwise, preserve the order and contents of all remaining models.
7. Write the minimal change directly to `default.json` in a single in-memory edit. Preserve the existing JSON indentation, encoding, newline style, and unrelated content.
8. Re-parse the written file and confirm that the top-level `models` array is valid and that the intended entries are present. Do not perform unrelated checks.

Do not run the models. Do not call `codex exec`, `codex`, or any provider request as part of this skill.

## Reporting

Tell the user:

- The `default.json` path that was modified.
- The model slugs added, changed, or removed.
- The fields changed for each model.
- That the written file parses as valid JSON.

Do not claim that a model works or that a provider supports it. A catalog entry is a local list entry, not proof of provider availability or entitlement.

## Boundaries

- Write only `default.json`. Do not create backups, temp files, or any other file during the change.
- Never modify `config.toml`.
- Never create a timestamped or other backup of `default.json`.
- Never replace the user's catalog with `assets/default.json`.
- Do not require Python, Node.js, or a management script.
- Do not expose credentials or include secrets in output.
