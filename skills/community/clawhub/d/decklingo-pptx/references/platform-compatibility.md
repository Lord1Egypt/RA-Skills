# Platform Compatibility

DeckLingo for PPTX is intentionally runtime-agnostic.

## Works Well In

- Codex-style skill runtimes that load `SKILL.md` and run local scripts
- OpenClaw-style local agent platforms that can mount a skill/tool directory
- Other agent systems that support:
  - markdown instructions
  - local Python execution
  - access to PPTX files on disk

## Minimum Runtime Requirements

- Python 3.10+
- `lxml`
- `deep-translator`
- zip read/write access

## Packaging Guidance

- Keep the skill directory self-contained
- Preserve relative paths under `agents/`, `assets/`, `references/`, and `scripts/`
- Treat `scripts/translate_pptx_text.py` as the main entrypoint
- Treat `scripts/scan_pptx_text.py` as the preflight entrypoint

## Notes For OpenClaw-Like Platforms

- If the platform does not read `agents/openai.yaml`, the skill still works through `SKILL.md` plus the scripts
- If the platform has its own marketplace manifest format, reuse:
  - display name: DeckLingo for PPTX
  - short description: Translate editable PPTX decks with glossary-aware verification
  - icon assets from `assets/`
