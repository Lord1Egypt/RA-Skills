# Releasing

## Release checklist

1. Update `CHANGELOG.md` under a new version heading.
2. Verify cross-framework files are aligned:
   - `prompts/core-rules.md`
   - `prompts/claude-project.md`
   - `prompts/openclaw-system.md`
   - `.cursor/skills/bangboo-voice/SKILL.md`
3. Confirm lexicon integrity in `.cursor/skills/bangboo-voice/reference-lexicon.md`.
4. Commit changes and tag a semantic version (`vX.Y.Z`).
5. Publish GitHub Release with:
   - summary,
   - compatibility notes (Cursor/Claude/OpenClaw),
   - migration notes (if any).

## Suggested tag strategy

- `v1.0.0`: initial public stable release.
- `v1.1.0`: backward-compatible new prompt features.
- `v1.1.1`: typo/documentation/non-breaking fixes.
