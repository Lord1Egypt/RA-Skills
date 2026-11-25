# Changelog

## 1.2.0 — 2026-11-24

- `quota`: remaining quota for Codex (session logs), Claude Code (`/usage` cache, refreshed in a hidden terminal) and agy (its own status-line data). Local reads only; `CREW_NO_QUOTA=1` turns them off.
- `advise --task <type>`: recommends a model from quota, a leaderboard snapshot and personal preferences, with reasons.
- `rankings`: status / show / import / schema for `~/.config/crew/rankings.json`; the main agent refreshes it from arena.ai when older than 30 days.
- Personal preferences in `~/.config/crew/roles.json` (task → preferred models, thresholds, Claude menu).
- `models` shows remaining quota per option and lists only installed CLIs; `spawn` warns when the chosen model's quota is below 20%.
- `doctor`: checks dependencies, model lists, quota sources and config.
- Leaderboard matching compares dotted versions correctly (4.6 < 5) and never lets an older model stand in for the one an alias starts.
- agy menu no longer hides any family; the menu is simply each CLI's first two models.
- Bilingual: English + Chinese description, an English overview at the top of SKILL.md (agents reply in the user's language), full English README (`README.en.md`).
- Scope stated plainly: macOS + iTerm2; Claude Code, Codex and agy.
- ClawHub metadata (`metadata.openclaw`), permissions and privacy section, MIT-0 license.

Verified with Claude Code 2.1.331, codex-cli 0.172.0, agy 1.5.16 on macOS (python3 3.9 and 3.13).
