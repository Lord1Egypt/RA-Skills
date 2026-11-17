# Changelog

## [1.1.0] - 2026-10-31

### Security
- Secret values are never written to reports or the console (1.0 copied raw snippets of keys into the report). Findings show file, line, key name, type and length only.
- Home-directory paths are shown as `~` so reports do not reveal the OS username.
- HTML report escapes all content and ships a strict Content-Security-Policy.
- Removed generated reports from the package; added `.gitignore` for reports, `config.json` and `.env`.

### Fixed
- PERM001: real Windows ACL check via `icacls`; POSIX check flags group/other access. Locked or unreadable files no longer fail the check.
- CRYPTO001: bounded, error-tolerant walker; long Windows paths, junction loops and `node_modules` no longer crash it. Removed substring check that matched "des" in "description".
- SEC003: scans added lines in the last 50 commits instead of `--stat` output; `--git-repo` option.
- NET001: runs netstat once, separates ports exposed on all interfaces from loopback-only; tunnel detection works on Windows.
- CFG001: replaced false-positive "missing config" warning with real OpenClaw risk checks (bind, auth, open DMs, wildcard allowlists, exec without approvals).
- `--check` now runs only the requested check; config toggles in `checks` actually disable checks; `info` status counted.

### Changed
- Standard library only; `requests`, `rich`, `jsonschema`, `pyyaml` no longer needed. Python 3.8+.
- Supply-chain scan covers several skill folders and SKILL.md `curl | sh` patterns.

## [1.0.0] - 2026-10-31
- Initial version.
