# Changelog

All notable changes to the `airbnb-gateway` skill package. Format follows
[Keep a Changelog](https://keepachangelog.com/); versions follow SemVer.

## [Unreleased]

### Changed
- v0.1.4: Added a friendly "star this skill" call-to-action to `SKILL.md`,
  `README.md`, and `CLAWHUB.md` (shown on the ClawHub listing) — content-only,
  no behavior change.
- v0.1.3: Clean re-cut for review handoff — no content or doctrine change since
  v0.1.2; published to give the reviewing agent a fresh version number to pin
  its install/audit against.
- v0.1.2: Pre-install polish pass (no doctrine change). Replaced the
  "Capabilities this skill expects" section with an explicit **Minimum
  Environment Contract** (read-only minimum vs send-capable minimum vs optional
  enhancements) so outside users can tell at a glance whether the skill can run.
  Converted the **Command surface** table to a renderer-safe bullet list (the
  `<id>`/`<thread>` placeholders rendered as collapsed on some markdown
  platforms). Verified package completeness: all `references/` and `examples/`
  files ship in the published artifact — the ClawHub web page previews only
  `SKILL.md`, but installs are complete.
- v0.1.1: Rewrote the `SKILL.md` frontmatter `description` to match the ClawHub
  listing blurb (`CLAWHUB.md`), so the published summary reads in the intended
  voice instead of the long internal one-liner.

### Added
- Initial `airbnb-gateway` skill package (v0.1.0):
  - `SKILL.md` — operating contract: Five Laws, tier-based operating model,
    safety tiers, send state machine, command surface, anti-patterns,
    future-adapter section, maintainer notes.
  - `references/airbnb-message-state-machine.md` — full send state machine,
    dedupe key, ledger contract, verify window, edge cases.
  - `references/airbnb-tool-priority.md` — the one per-deployment file: tier
    order + role→tool map + degradation matrix.
  - `references/airbnb-safety-rules.md` — READ/WRITE/MUTATE tiers, approval gate,
    ambiguity handling, escalation report shape, observability.
  - `references/future-adapter-interface.md` — ideal adapter functions and how
    the skill should call them when present.
  - `examples/` — check-inbox, read-thread, send-reply-with-verification
    (incl. the no-resend `unconfirmed` path), reservation-lookup,
    calendar-inspection.
  - `state/send-log.schema.json` — append-only dedupe ledger schema.
  - `README.md`, `LICENSE` (MIT) — Open Hub-friendly packaging.
  - `CLAWHUB.md` — verbatim ClawHub/Open Hub listing description.

### Notes
- Scope is read operations + verified single-send. Calendar/pricing/listing
  mutations are intentionally refused (escalate) until v2.
