# Release Notes — skill-inventory v1.5.2

**Release date**: 2026-10-14
**Package**: `skill-inventory-1.5.2-tianxi.zip` (for Tianxi AI / 天禧 AI skill square)
**Head**: `df01c66` (repo) + Tianxi-publish remediation (config/CHANGELOG/RELEASE_NOTES/.skill-config.json/packaging)

## What's new in 1.5.2

This release is a **publish-readiness hardening pass** for the Tianxi AI skill square, plus the
carried-over non-blocking code-audit fixes. No runtime behavior changed for end users.

### Tianxi (天禧 AI) publish readiness
- Version markers across `SKILL.md` / `config.yaml` / `SKILL.en.md` are now consistent at `1.5.2`.
- The contradictory `config.yaml` `filesystem: read-only` claim is gone from the upload package
  (the skill does perform two disclosed, consent-gated writes). `config.yaml` is excluded from the
  zip — it is a local archive file, not an official upload requirement.
- A deterministic white-list packaging script (`tools/build_tianxi_zip.py`) replaces the stale
  `v1.4.0` package and runs a post-pack safety scan (zero networking / subprocess keywords in any
  bundled `.py`; valid `SKILL.md` YAML frontmatter).
- Docs now state explicitly that Tianxi AI is supported **via generic agent mode** — no proprietary
  profile is claimed.
- Added `CHANGELOG.md` / `RELEASE_NOTES.md` and a private, git-ignored `.skill-config.json` for the
  `lenovoskill` CLI.

### Code quality (from audit remediation)
- Removed cross-invocation global state leakage in the protection / safety-heuristic path.
- `backup_settings()` returns a single path; backup timestamp is microsecond-precise.
- `rows` schema documented; i18n template `.format()` self-test added (206 templates).

## Compatibility
- Pure local static analysis. **No network, no subprocesses** — safe for sandboxed upload review.
- Supported scan targets: WorkBuddy, QwenWork, Baidu DuMate, **Tianxi AI (via `generic` mode)**,
  and any host via `--root <dir>` / `--probe`.
- Default read-only. Two disclosed, consent-gated write paths (`--overrides --apply --yes`,
  `--set-lang`) plus one disclosed backup artifact before the close write.

## Upgrade note
Replace any previously uploaded package with `skill-inventory-1.5.2-tianxi.zip`. No user-data
migration required.
