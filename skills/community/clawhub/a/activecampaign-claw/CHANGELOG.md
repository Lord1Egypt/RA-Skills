# Changelog

All notable changes to this skill are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.9.4] — 2026-06-04

### Changed
- Cleanup.

## [1.9.3] — 2026-06-04

### Changed
- Cleanup.

## [1.9.2] — 2026-06-04

### Changed
- Cleanup.

## [1.9.1] — 2026-06-04

### Fixed
- `cli_main` 403 / `feature_unavailable` path now respects `--format json` and emits a `{"unavailable": true, "feature": ..., "plan_required": ..., "reason": ...}` sentinel instead of always printing the markdown block. Pipelines downstream that expect JSON were getting markdown when hitting a plan-tier-gated endpoint on Lite accounts.
- 1 new unit test locking the JSON-on-403 contract.

## [1.9.0] — 2026-06-04

### Added
- `cli_main()` now exposes `args.progress(msg)` — a callable scripts can invoke to emit per-step progress lines to stderr. Auto-silenced in three cases: `--quiet` flag, `TELEGRAM_QUIET=1` env var, or when stderr isn't a tty (the common case when output is piped or captured by a Telegram bridge).
- Progress wired into `tag_audit.py` (streaming pair count) and `contact_full_profile.py` (parallel sub-resource fetches).
- 4 new unit tests covering the four progress modes (tty-emits, `--quiet`-silences, `TELEGRAM_QUIET=1`-silences, non-tty-silences).

### Why
- Telegram users were seeing tool-use breadcrumbs and stderr noise pollute their replies. Progress was always there in some scripts via raw `sys.stderr.write` calls, but inconsistent and unsuppressable. The new centralized callback makes "show progress" / "stay silent" a per-invocation choice with sensible defaults.

## [1.8.0] — 2026-06-04

### Added
- 4 new scripts that fan multi-endpoint reads out in parallel via `fetch_many`:
  - `contact_most_engaged.py` — top N contacts by score (default) or by recent activity (`--by recent`). Single API call. Plugs the gap that was previously triggering inline-Python fallbacks for "most engaged" questions.
  - `contact_full_profile.py --email|--id` — one report with contact + tags + lists + automations + custom fields + deals + notes, all pulled concurrently. ~4–5s instead of 6 serial script invocations.
  - `deal_full_context.py <id>` — deal + contact + tasks + notes + custom fields in one report.
  - `automation_deep_dive.py <id> [--max-enrollments N]` — automation metadata + per-step funnel + enrollment status breakdown.
- 10 new unit tests + 16 smoke tests covering analyze + render shapes and the per-endpoint 403 sentinel handling.

### Changed
- **Critical operating rule #13 tightened** — inline `python3 -c` / `python3 - <<'PY'` heredocs are now explicitly **forbidden**, not just discouraged. The previous wording said "prefer the named scripts," which the agent was interpreting as "OK to write ad-hoc Python when a script doesn't perfectly match." Tightened to: never write inline Python; if no exact-match script exists, run the closest one. The Telegram tool-use breadcrumb leaks heredoc bodies verbatim to the user — using named scripts keeps the breadcrumb to one short line.
- Rule #13 now includes a common-question → script mapping for the most-asked patterns (`contact_recent`, `contact_most_engaged`, `contact_lookup`, etc.).
- SKILL.md "Quick lookups" decision-tree table extended with the new compound scripts.

## [1.7.0] — 2026-06-04

### Added
- 7 quick-lookup scripts for single-record questions, each a single API call with sub-second runtime: `contact_lookup.py --email`, `contact_recent.py [--limit N]`, `contact_by_id.py <id>`, `deal_by_id.py <id>`, `tag_lookup.py --name <name>`, `automation_lookup.py --name <name>`, `last_campaign.py`.
- `tag_lookup` and `automation_lookup` check `state.json` first and only fall back to the API when the local taxonomy doesn't already have the answer.
- 17 new unit tests + 24 smoke tests (auto-discovered for the 7 new scripts) covering analyze + render + state-first paths.

### Changed
- SKILL.md decision tree — added a "Quick lookups" section at the top, instructing the agent to prefer these single-call scripts over the audit scripts whenever the user asks about one specific contact / deal / tag / automation / campaign. Reduces routing latency for the common "find / look up / what's the most recent" intent from 5–10s to ~500ms.

## [1.6.0] — 2026-06-03

### Added
- OS keychain support for `AC_API_URL` and `AC_API_TOKEN` via the optional `keyring` package. Without `keyring` installed, the skill continues to work exactly as before.
- `_skill/secrets.py` — credential resolver that checks env vars first, then the keychain. Env vars always win when both are set (so sandbox testing isn't disrupted by production credentials in the keychain).
- `scripts/auth.py` — manage credentials in the OS keychain: `status`, `set <url> <token>`, `set-url <url>`, `set-token <token>`, `clear`. Friendly handling for the macOS Keychain non-interactive write-error case.
- Optional `[keychain]` extra in `pyproject.toml` — install with `pip install 'activecampaign-claw[keychain]'` or directly `pip install keyring`.
- 10 new unit tests covering env-vs-keychain precedence, graceful degradation when `keyring` isn't installed, empty-env fallthrough, and `describe_sources` reporting.

### Changed
- `ACClient.__init__` — error message now points to `python3 scripts/auth.py status` so users can diagnose where (or whether) credentials are configured.
- INSTALL.md — added "Option C — OS keychain" alongside the existing env var and OpenClaw config paths.

## [1.5.1] — 2026-06-03

### Changed
- Ported 22 additional scripts to the `cli_main()` driver from 1.5.0: `automation_audit`, `automation_dependency_map`, `automation_overlap`, `broken_automation_detector`, `campaign_velocity`, `contact_completeness_report`, `content_length_report`, `custom_field_audit`, `domain_engagement_report`, `engagement_decay`, `form_audit`, `from_name_report`, `link_performance`, `list_audit`, `list_overlap`, `new_subscriber_quality`, `segment_audit`, `send_frequency_report`, `stale_contact_report`, `stalled_automations`, `tag_audit`, `unsubscribe_audit`. 25 scripts now use the consolidated driver.
- Each ported script's `main()` dropped from ~15–25 lines of argparse + flow boilerplate to ~6–12 lines of declarative configuration. Behavior is unchanged.
- Restored `--max-items` declarations on 8 scripts where the automated porter dropped them from the argparse layer while keeping them in the fetch wiring.

## [1.5.0] — 2026-06-03

### Added
- `_skill/cli.py` — `cli_main()` driver that handles the common analysis-script boilerplate: argparse with standard `--format` and `--output` flags, `ACClient` instantiation, fetch → analyze → render → write flow, optional 403 → friendly-markdown handling, optional `emit_files()` trailer on output, optional `history.jsonl` logging. Re-exported from `_ac_client` so scripts opt in with `from _ac_client import cli_main`.
- Pilot ports: `accounts_audit.py`, `tasks_audit.py`, `template_audit.py` now use `cli_main()` instead of writing their own main(). Their `main()` functions drop from ~20 lines of boilerplate to ~10 lines of declarative configuration.
- 7 unit tests covering the cli_main happy path, `--format json`, `--output` + trailer emission, custom argparse arguments via the `add_arguments` callback, friendly 403 handling, propagation of non-403 errors, and history-recipe logging.

### Notes
- This is an opt-in helper, not a forced migration. The other 55 scripts are unchanged. Incremental adoption is expected.
- `analyze` functions are detected as args-aware only when their signature includes a parameter literally named `args`. This avoids accidentally injecting the argparse `Namespace` into a parameter the script intended for something else (e.g., a `now=None` clock injector).

## [1.4.1] — 2026-06-03

### Changed
- `tag_audit.py` — `fetch_data()` now streams `/contactTags` and pre-aggregates into a `Counter` + per-contact tag sets, instead of materializing the full 50k-row list. Memory bound is now ~1–2 orders of magnitude smaller on accounts with many contact-tag pairs. `analyze()` accepts either the new pre-aggregated shape or the legacy raw list for backward compatibility with existing tests and callers.
- Lowered aggressive `max_items` defaults: `list_overlap.py` 200000 → 50000, `list_audit.py` 100000 → 50000, `win_loss_report.py` 100000 → 50000, `export_account.py` 200000 → 50000 (on the four highest-volume sub-resources).
- Added `--max-items` CLI flag to 10 scripts that previously had only a hardcoded default: `automation_audit`, `automation_overlap`, `stalled_automations`, `bounce_breakdown`, `list_audit`, `list_overlap`, `list_growth_forecast`, `domain_engagement_report`, `send_frequency_report`, `notes_analysis`. Plus `tag_audit` gained the same flag wired into its streaming fetch.

### Added
- Test asserting `tag_audit.analyze()` works on the new pre-aggregated shape (alongside the existing list-shape tests).

## [1.4.0] — 2026-06-03

### Added
- `Makefile` with `test`, `lint`, `verify`, `release`, and `publish` targets. `make release VERSION=x.y.z` bumps version files, commits, and creates a `v<version>` git tag locally so every release is identifiable in history.
- `.github/dependabot.yml` — weekly checks for GitHub Actions and pip dependency updates.
- `.github/workflows/codeql.yml` — CodeQL static analysis on every push, PR, and weekly schedule.
- `_skill/schemas.py` — `TypedDict`s for `Contact`, `Deal`, `Campaign`, `Tag`, `User`, `DealTask`, `Note` covering the documented AC v3 record shapes. Re-exported from `_ac_client` for opt-in adoption by new code.
- Snapshot-style renderer tests in `tests/test_render_snapshots.py` that assert full markdown output (not just substring presence), catching silent formatting drift.

### Changed
- CI matrix trimmed: ubuntu-latest only on Python 3.9 + 3.12 (was ubuntu+macos × 4 Python versions). 8 jobs → 2 jobs per push.

## [1.3.1] — 2026-06-03

### Added
- `ACClient.fetch_many()` — concurrent multi-endpoint pagination via `ThreadPoolExecutor`. Each request keeps its own label; per-endpoint errors are returned as sentinels so a single failure doesn't break sibling fetches.
- Thread-safe `_throttle()` (now wrapped in a per-client lock). Multiple concurrent callers stay correctly spaced at 5 req/sec.
- `--max-aux` flag on `find_hot_leads.py` (default 50000) to bound the bulk `/scoreValues` and `/contactTags` pulls. Replaces the previous hardcoded 200000.

### Changed
- `data_subject_export.py` — refactored to use `fetch_many` for its five per-contact subresource pulls. Parses + indexes in parallel where the rate limit allows.

### Fixed
- Test fixtures that constructed an `ACClient` via `__new__` now initialize `_throttle_lock`, `_write_count`, `_max_writes`, and `_read_only` so the new client-state additions don't break out-of-band construction.

## [1.3.0] — 2026-06-03

### Added
- `ACClient.write()` — single audited code path for POST / PUT / DELETE. All write methods now route through it.
- `AC_READ_ONLY=1` env var. When set, every write is refused at the client layer before any HTTPS request goes out. Reads still work normally. Lets you run any analysis without modification risk.
- `AC_MAX_WRITES=<n>` env var. Default is 10 modifications per process invocation; can be overridden per-run when intended.
- Write audit log at `~/.activecampaign-skill/writes.jsonl` (file mode 0600). Records timestamp, endpoint, method, payload SHA-256 (not the payload itself), invoking script, and sequence number.
- New `ReadOnlyModeError` and `WriteCapExceededError` exception types, re-exported from `_ac_client`.
- 16 new unit tests covering the read-only path, per-process cap (default + override + cross-method counting), audit log shape (payload-hash, not payload), and best-effort log-failure tolerance.

## [1.2.0] — 2026-06-03

### Changed
- Internal refactor of `_ac_client.py` — implementation split into a `_skill/` sub-package (`client.py`, `state.py`, `history.py`, `reports.py`, `dates.py`, `safety.py`). `_ac_client.py` is now a thin facade that re-exports the public surface; all 58 scripts keep their existing imports unchanged.
- Consolidated `_parse_date`, `_safe_int`, `_safe_float` helpers (previously duplicated across 22 scripts) into `_skill/dates.py`. Scripts now import canonical versions from `_ac_client`.
- Standardized voice on user-facing input/scope messages — `send_simulator.py` and `tag_merge.py` no longer use `"ERROR:"` prefixes for non-error UX paths (missing scope flag, friendly merge-validation messages).

## [1.1.4] — 2026-06-03

### Changed
- `find_hot_leads.py` — switched to bulk `/scoreValues` + `/contactTags` joins with a client-side index, replacing the per-contact subresource pattern. Added `--max-contacts` flag (default 5000) for runtime control. The script also tolerates a 403 on `/deals` and continues with score + tag signals only.
- `find_slipping_deals.py` — routes a 403 on `/deals` through the shared `render_feature_unavailable` helper for consistent voice with the other Deals-dependent scripts.
- `segment_performance.py` — when invoked without `--list`, `--tag`, or `--segment`, prints a multi-line markdown block explaining the audience-scope requirement and points at the relevant audit scripts for finding ids. Exits cleanly rather than raising.
- 7 new unit tests covering the bulk-endpoint join, the `--max-contacts` cap, plan-gating fallbacks, and the friendly audience-scope message.

## [1.1.3] — 2026-06-02

### Changed
- Display-name refresh.

## [1.1.2] — 2026-05-05

### Changed
- Documentation polish.

## [1.1.1] — 2026-05-05

### Changed
- Documentation polish.

## [1.1.0] — 2026-05-05

### Added
- `scripts/tasks_audit.py` — overdue tasks, completion rate per user, unassigned tasks. Uses `/dealTasks` with `filters[reltype]=Deal|Subscriber` (covers contact tasks too — there is no separate `/contactTasks` endpoint in v3). Exits cleanly on 403 for non-Plus accounts.
- `scripts/notes_analysis.py` — content analysis across `/notes`: action-item extraction, per-user note count + median length, stale-note flag for deals, top recurring vocabulary.
- `scripts/sales_rep_performance.py` — per-rep scoreboard combining `/users`, `/deals`, `/dealTasks`, `/notes`: open / won / lost deals, win rate, avg won value, open + overdue tasks, notes count, composite activity score. Falls back to notes-only view on Lite plans (no /deals).
- `scripts/template_audit.py` — campaign template audit using `/templates` cross-referenced with `/campaigns`: unused, stale, per-template avg open rate, length-distribution outliers.
- `scripts/saved_responses_audit.py` — sales-reply library audit using `/savedResponses` (Plus+): stale entries, length outliers, near-duplicate detection via jaccard on tokenized HTML-stripped bodies.
- `scripts/accounts_audit.py` — B2B Accounts audit (Plus+) using `/accounts` (with `count_deals=true`) + `/accountContacts`: orphaned accounts, no-pipeline accounts, top accounts by deals/contacts, per-owner rollup. Exits cleanly on 403 if the Accounts feature isn't enabled.
- `scripts/forms_lead_quality.py` — per-form lead quality reconstructed from each form's `subscribelist` membership + recent engagement events. Caveat documented inline: AC v3 has no `/formSubmissions` endpoint, so this is a list-quality reading rather than a strict per-submission reading when a list has multiple opt-in sources.
- 36 new unit tests + 28 smoke tests across the 7 new scripts. Fixtures match the JSON shapes documented in the AC v3 reference for `/dealTasks`, `/notes`, `/users`, `/templates`, `/savedResponses`, `/accounts`, `/accountContacts`, and `/forms`.

### Changed
- README "What it can do" — added the Sales / CRM section and a Marketing-content hygiene section.
- SKILL.md — added a "Sales / CRM scripts" decision-tree row group.

## [1.0.20] — 2026-05-05

### Changed
- Documentation polish.

## [1.0.19] — 2026-05-05

### Changed
- Restructured top of SKILL.md so the marketplace listing leads with user-facing content: tagline → "What it does" (capabilities by category) → "Examples" → "What makes this skill different" → "Setup". The agent-routing sections ("Use this skill when..." / "Do NOT use this skill when...") moved down into a single "When to invoke this skill" section right before "Critical operating rules", where they belong as agent spec.

## [1.0.18] — 2026-05-05

### Changed
- Removed the "READ FIRST — Response format rules" preamble from the top of SKILL.md. Its content (R1/R2/R3) was already restated by rules 12 and 13 under "Critical operating rules" further down. The preamble was dominating the clawhub.ai listing page; deleting the duplicate lets the listing lead with the human-facing intro.
- Removed the coverage badge from README.md.

## [1.0.17] — 2026-04-26

### Added
- `_ac_client.emit_files(*paths)` — prints a structured trailer line `__SKILL_FILES__:[...]` (JSON array of absolute paths) so the agent has a deterministic landmark to grep for instead of hunting through prose. 3 new tests cover trailer format, multi-path emission, and JSON validity.
- New "READ FIRST — Response format rules" preamble at the top of SKILL.md (rules R1–R3). Restates the most-violated rules above the decision tree so they get attention earlier in the prompt. Lists every observed forbidden trailing-label variant explicitly: `Files:`, `Output:`, `Current snapshot:`, `Latest pointer:`, `Saved to:`, `Backup record:`, `Results:`, `I saved the [thing] here:`.

### Changed
- `snapshot.py`, `suppression_export.py`, `export_account.py`, `data_subject_export.py`, `audit_list_health.py`, `find_hot_leads.py` now call `emit_files()` after writing their output files. Existing `Wrote /path` lines are preserved for backwards-compat.
- Rule #12 updated to reference the structured trailer alongside the human-readable `Wrote ` lines.

## [1.0.16] — 2026-04-26

### Changed
- Strengthened SKILL.md rule #12 with two new hard rules:
  - **Pass through `Wrote /path` lines verbatim.** Every script that writes a file prints these to stdout; the agent must scan for `Wrote `, `Saved to `, `Output:` substrings and reproduce every match in the response.
  - **Forbidden trailing labels enumerated explicitly.** `Files:`, `Output:`, `Current snapshot:`, `Latest pointer:`, `Saved to:`, `Results:`, etc. — any of these followed by no content marks the response as broken.
- Added a real "snapshot trail-off" example pulled from observed agent output, with both bad and good versions including the actual `~/.activecampaign-skill/snapshots/...json`, `manifest.jsonl`, and LaunchAgent paths.
- Codified required response structure for file-writing scripts: 1-line summary → enumerated paths → 2-3 line content summary → next-step offer.

## [1.0.15] — 2026-04-26

### Changed
- Generalized SKILL.md rule #12 to catch any trailing-label/colon pattern, not just `"saved here:"`. The previous wording missed the `"Files:"` variant observed in suppression_export. Rule now: any line introducing output (`Files:`, `Output:`, `Results:`, `Saved to:`, etc.) must be followed by the actual content in the same response. Includes "list every file path" requirement for multi-file exports and an explicit "no files written — output printed inline above" fallback for stdout-only scripts.

## [1.0.14] — 2026-04-26

### Added
- SKILL.md operating rule #13: always prefer named scripts in `scripts/` over inline Python heredocs. Reasons: scripts handle pagination, rate limits, retries, sanitization, history logging, and consistent markdown — ad-hoc inline Python skips all of that and dumps raw heredoc text to the harness progress line.
- SKILL.md operating rule #14: narrate before exec. Before running anything, say one human sentence describing what you're about to do, so the user has something readable to anchor on while the harness's technical progress line ("exec → python3 …") fires.

## [1.0.13] — 2026-04-26

### Added
- New SKILL.md operating rule (#12): when the agent saves a file, the response must include the absolute path AND a content summary on the same line. Fixes responses that ended mid-sentence with "I saved the audit here:" and no path. Includes good/bad examples.

## [1.0.12] — 2026-04-26

### Added
- 26 new `render_markdown()` tests across previously-untested scripts: `automation_audit`, `automation_funnel`, `automation_overlap`, `baseline_drift`, `broken_automation_detector`, `campaign_postmortem`, `campaign_velocity`, `contact_completeness_report`, `content_length_report`, `domain_engagement_report`, `engagement_decay`, `form_audit`, `from_name_report`, `link_performance`, `list_audit`, `list_growth_forecast`, `list_overlap`, `monthly_performance`, `mql_to_sql_handoff`, `new_subscriber_quality`, `send_frequency_report`, `stale_contact_report`, `stalled_automations`, `subject_line_report`, `unsubscribe_audit`, `win_loss_report`.
- 9 new `main()` integration tests in `tests/test_main_integration.py` covering the most-used scripts: `import_validator`, `audit_list_health`, `find_hot_leads`, `dedupe_contacts`, `tag_merge`. Each patches `sys.argv`, mocks `ACClient` where needed, runs `main()`, and verifies output. Also covers error paths (missing CSV, unknown source tag).

### Changed
- Coverage: 59% → 66%. Test count: 455 → 490.

## [1.0.11] — 2026-04-26

### Changed
- `dedupe_contacts.py` now uses `stream()` with slim records (id + email only) keyed by email/phone/name. Singletons sit in lookup maps until promoted to the duplicate output; full records never accumulate. Peak memory drops from ~1.5–2 GB on 1M-contact accounts to ~150 MB. `find_duplicates()` accepts any iterable; return dict now includes a `scanned` count.
- SCALING.md: documented why `audit_list_health` (already sample-bounded) and `contact_completeness_report` (streaming would force a 600× slowdown via per-contact field-value lookups) are intentionally still buffered.

### Added
- 3 new tests for `dedupe_contacts`: accepts a generator input, drops singletons from the output, and stores slim records only.

## [1.0.10] — 2026-04-26

### Added
- `ACClient.stream(path, key, params, limit_per_page, max_items)` — generator that yields records one at a time. `paginate()` is now a thin wrapper around it (`return list(self.stream(...))`); behavior unchanged for existing callers.

### Changed
- `role_address_finder.py`, `free_vs_corporate_report.py`, `stale_contact_report.py` now use `stream()` for the contact scan. Memory peak drops from O(N) to <1 MB regardless of contact count. `stale_contact_report.analyze()` also bounds its output samples to 50 records (counts come from explicit counters).
- SCALING.md updated with the new memory profile and remaining adoption gaps.

## [1.0.9] — 2026-04-26

### Changed
- Replaced the single bare-bones "Example agent interaction" in README with two concrete examples that show range: hot-leads ranking (analysis) and tag merge (maintenance with destructive-op confirm flow).

## [1.0.8] — 2026-04-26

### Changed
- Excluded `.github/` from the published bundle (workflow files are only used by the GitHub repo).

## [1.0.7] — 2026-04-26

### Added
- `scripts/tag_merge.py` — merges a source tag into a canonical target. Re-tags affected contacts, detects automation and segment references, deletes the source tag. Dry-run by default; `--confirm` required for execution.
- `recipes/re-engagement-launch.md` — workflow for designing and launching a re-engagement campaign.
- `recipes/monthly-deliverability-review.md` — monthly cadence for checking sender health.
- `recipes/pre-import-checklist.md` — pre-flight checks to run before importing a contact CSV.

### Changed
- Backfilled changelog entries for 1.0.1 through 1.0.6.

## [1.0.6] — 2026-04-26

### Fixed
- `SCALING.md` was referenced from README but missed the 1.0.5 commit; included now.

## [1.0.5] — 2026-04-26

### Added
- `SCALING.md` — runtime/memory math, per-script default caps, recommended workflows for 100k+ contact accounts, and known-not-yet-optimized items.
- README "Performance & scale" section linking to SCALING.md.

## [1.0.4] — 2026-04-26

### Added
- README intro and "Why this exists" section rewritten to focus on what the skill unlocks via the v3 API.
- Renamed README "What it can't do" section to "API scope" and reframed each bullet.

### Changed
- License badge updated to MIT-0; release badge bumped.
- License footer updated to MIT-0.

### Fixed
- Cleaned up 135 ruff lint errors:
  - Auto-fix: 95 (unused imports, sort order, redundant open modes, f-strings without placeholders).
  - Renamed ambiguous single-letter `l` loop variables across 12 scripts and 1 test.
  - Dropped assigned-but-unused locals across 6 scripts and 3 tests.
  - Added `from e` / `from None` to ACClientError raises in `_ac_client.py` and three downstream scripts.
  - Suppressed UP036 on the runtime Python>=3.9 check (kept as a friendly error for users running scripts directly).
  - Removed a no-op for-loop in `list_growth_forecast.py`.

## [1.0.3] — 2026-04-26

### Changed
- Wording cleanup across docs and examples; minor adjustment to the role-address local-part blocklist.

## [1.0.2] — 2026-04-26

### Changed
- Dropped the `(be honest about these)` aside from the SKILL.md "API limitations" heading.

## [1.0.1] — 2026-04-26

### Changed
- Wording polish in `SECURITY.md`, `tests/fixtures/mock_responses.py`, and `recipes/welcome-series.md`.

## [1.0.0] — 2026-04-26

### Added — initial public release

**Performance analysis (24 scripts):** `campaign_postmortem`, `campaign_compare`, `link_performance`, `bounce_breakdown`, `monthly_performance`, `baseline_drift`, `campaign_velocity`, `subject_line_report`, `content_length_report`, `from_name_report`, `send_time_optimizer`, `send_frequency_report`, `domain_engagement_report`, `engagement_decay`, `stale_contact_report`, `new_subscriber_quality`, `segment_performance`, `automation_audit`, `automation_funnel`, `automation_overlap`, `stalled_automations`, `form_audit`, `mql_to_sql_handoff`, `win_loss_report`.

**Operational / hygiene (16 scripts):** `tag_audit`, `custom_field_audit`, `list_audit`, `list_overlap`, `segment_audit`, `pipeline_audit`, `automation_dependency_map`, `broken_automation_detector`, `dedupe_contacts`, `contact_completeness_report`, `role_address_finder`, `free_vs_corporate_report`, `import_validator`, `webhook_audit`, `unsubscribe_audit`, `suppression_export`.

**Compliance / migration (4 scripts):** `data_subject_export`, `export_account`, `snapshot`, `schema_diff`.

**Forecasting (2 scripts):** `send_simulator`, `list_growth_forecast`.

**Pre-existing (carried forward):** `calibrate`, `audit_list_health`, `find_hot_leads`, `find_slipping_deals`.

**Workflow recipes:** `recipes/daily-digest.md`, `recipes/deal-hygiene.md`, `recipes/list-health-audit.md`, `recipes/welcome-series.md`.

**Frameworks:** `frameworks/email-best-practices.md`, `frameworks/segmentation-theory.md`.

**API references:** `references/contacts.md`, `references/deals.md`, `references/custom-fields.md`.

### Notes on AC API limits

- `/messageActivities` is not exposed on every plan. Engagement scripts fall back to `/linkData` (clicks-only) automatically.
- Deals-dependent scripts (`pipeline_audit`, `mql_to_sql_handoff`, `win_loss_report`) require the Deals feature.
- The skill cannot send campaigns or create automations — those AC v3 endpoints don't exist; the skill produces specs.
