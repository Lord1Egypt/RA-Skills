# audit-openclaw-security v2

This bundle updates the original skill for current OpenClaw and current Agent Skills / OpenClaw skill-loader expectations.

## Main changes

- migrated `SKILL.md` frontmatter to an OpenClaw-compatible form:
  - single-line frontmatter keys
  - inline JSON `metadata`
  - `{baseDir}` references for bundled scripts
- retuned the description so it is specific about both:
  - what the skill does
  - when it should trigger
- updated the audit workflow for current OpenClaw commands:
  - `openclaw status --deep`
  - `openclaw gateway probe --json`
  - `openclaw channels status --probe`
  - `openclaw backup create --verify`
- expanded the current audit-check glossary and check-id map
- added current reverse-proxy, Control UI origin, and Tailscale Serve/Funnel guidance
- added current `session.dmScope` guidance for shared inbox and multi-account setups
- refreshed platform playbooks
- upgraded bundled scripts for agentic use:
  - `--help` support
  - safer config redaction flow
  - richer rendered report with environment clues and merged audit findings

## Bundle versioning

- Canonical skill name remains `audit-openclaw-security` so the directory still matches the `name` field.
- Bundle metadata version is now `2.1.0`.
- Validated against OpenClaw `2026.3.8`.
