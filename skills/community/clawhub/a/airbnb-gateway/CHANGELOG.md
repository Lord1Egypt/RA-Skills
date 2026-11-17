# Changelog

All notable changes to the `airbnb-gateway` skill package. Format follows
[Keep a Changelog](https://keepachangelog.com/); versions follow SemVer.

## [Unreleased]

### Fixed
- v0.2.1: **Doc-consistency reconciliation (resolves NVIDIA SkillSpector
  findings).** The v0.2.0 approval-gated calendar-mutation capability had left
  stale v1 "calendar is read-only / mutation reserved for v2 / refuse + escalate"
  language in ~6 places, which the scanner flagged as description-behavior
  mismatch (×2), intent-code divergence (High), and a missing production-impact
  warning. Propagated the MUTATE-CAL (gated, permitted) vs MUTATE-RESTRICTED
  (refused) split everywhere: SKILL.md (frontmatter `description` now names the
  gated calendar-mutation capability; Law #5; renamed "Reservation & calendar
  (READ-only in v1)" → "Reservation & calendar reads" with a corrected scope
  paragraph), `references/airbnb-safety-rules.md` (split the MUTATE tier row +
  escalation triggers), `README.md` status, `examples/calendar-inspection.md`,
  and `references/future-adapter-interface.md`. Added a prominent
  **"⚠️ THIS CHANGES LIVE PRODUCTION INVENTORY"** warning to
  `references/calendar-mutation-procedure.md`. No behavior change — the gated
  write scope was already the intent; the docs now state it consistently.
- v0.2.1: `references/calendar-mutation-procedure.md` — added a
  **Context rule** (targeted evals / server-side grep instead of repeated full
  snapshots; a live run pulled 15+ full snapshots and stalled silently mid-task)
  and a **Completion rule** (a MUTATE-CAL turn must end with a report or an
  explicit unconfirmed/failure statement; NO_REPLY forbidden).
- v0.2.1: `references/calendar-mutation-procedure.md` — added a
  **Transport rule**: ClawBridge calls go through exec + curl ONLY; the built-in
  `fetch`/`web_fetch` tool can't send the Authorization header and internal
  hosts are blocked for it — it killed two live runs on 2026-07-04 at the
  verification step (agents drift to it under pressure; now explicitly
  forbidden, with a curl-pipe-grep pattern for snapshot searches).
- v0.2.1: `references/calendar-mutation-procedure.md` — added a
  **Payload rule**: never inline eval JS into a quoted `curl -d '...'` argument;
  write the JSON body to a file with the `write` tool and send `-d @file`.
  Root cause of the 2026-07-04 failed round-trip test: the eval scripts' single
  quotes broke shell quoting and curl exited 3 ("URL malformed") seven times in
  a row — the requests never reached ClawBridge. Also listed under Known traps.

### Changed
- v0.2.0: **Approval-gated calendar mutations.** Split the MUTATE tier into
  MUTATE-CAL (block/open dates, nightly price — permitted with explicit
  per-operation operator approval: APPROVED keyword, one op per approval,
  mandatory fresh-load verification after, reported inverse operation) and
  MUTATE-RESTRICTED (listing edits, accept/decline, refunds — still refuse +
  escalate). Added `references/calendar-mutation-procedure.md`, the live-verified
  step-by-step multicalendar procedure (animation-safe month navigation,
  JS event-dispatch date selection, availability radio + save, fresh-load
  verification), and `SKILL_CARD.md` (NVIDIA skill-card trust format with
  release evidence from the 2026-07-04 live round-trip test).
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
- Current scope (as of v0.2.x): read operations, verified single-send, and
  approval-gated **MUTATE-CAL** calendar mutations (block/open dates, nightly
  price — explicit per-operation operator approval + mandatory fresh-load
  verification + reported inverse). **MUTATE-RESTRICTED** operations (listing
  edits, accept/decline bookings, refunds, payouts) remain intentionally refused
  (escalate). (v0.1.0 originally shipped read + single-send only; calendar
  mutation was added under its gate in v0.2.0.)
