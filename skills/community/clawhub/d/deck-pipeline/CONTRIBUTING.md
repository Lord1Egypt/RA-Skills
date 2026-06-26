# Contributing

Thanks for your interest. This is a small, opinionated tool — contributions are welcome but please keep the surface area minimal.

## Reporting issues

Open a GitHub issue with:
- What you ran (command + relevant CLI flags)
- What you expected vs what happened
- A minimal reproduction (a sanitized 1–3 slide `.pptx` is ideal)
- Your environment (Python version, OS, `python-pptx` version)

Do **not** attach decks containing confidential content.

## Pull requests

1. Fork → branch from `main` → PR back into `main`.
2. Keep PRs focused. One concern per PR. Split if needed.
3. Touch the smallest possible surface.
4. Update `CHANGELOG.md` under `[Unreleased]` with a one-line summary.
5. If you change script behavior, update the corresponding section in `SKILL.md` and `README.md`.
6. New scripts must:
   - Be runnable standalone via `python3 <script>.py`.
   - Print a usage line when called with no args.
   - Honor `~$xxx` lock-file checks if they write `.pptx` / `.xlsx`.
   - Follow the existing scripts as style references.

## Design principles (please respect)

- **No silent guessing.** When unsure, stop and ask the user (the skill is bidirectional by design).
- **Discrete steps over bulk reductions.** Font compression goes by `-0.1pt`, never `-1pt` shortcuts.
- **Profile-agnostic core.** Anything organization-specific belongs in the `PROFILE` block in `SKILL.md`, never hardcoded in a script.
- **Reverse-syncable.** Excel companion files must support being updated from hand-edited PPTs, not just one-way generation.
- **Don't delete content.** Layout fixes use geometry / line-height / discrete font compression. If those fail, escalate to the user.

## Style references

Adding additional reference samples for style distillation is supported via `style_distill.py` and the `PROFILE.style_references` list. PRs that ship new bundled samples should:
- Use materials that are publicly distributable (no NDA / leaked content).
- Add a note in the `style_references` documentation describing the sample's origin and any usage caveats.

## Code of conduct

Be decent. Disagree on technical substance, not on the person.
