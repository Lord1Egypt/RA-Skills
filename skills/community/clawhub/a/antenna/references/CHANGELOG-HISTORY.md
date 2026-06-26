# Changelog

All notable changes to the Antenna skill are documented here.

## [Unreleased]

### Changed
- **Test-suite provider request compatibility and fixture freshness refresh.** `scripts/antenna-test-suite.sh` now sends OpenAI-family requests with `max_completion_tokens`, Anthropic requests with `max_tokens`, and uses a fresh current UTC timestamp in Tier A.15 so the REF-500 regression once again exercises session-target rejection instead of tripping freshness validation first. Fresh validation evidence now includes clean full-suite runs for `openai/gpt-5.4-nano`, `openai/gpt-5.4-mini-2026-03-17`, `anthropic/claude-sonnet-4-5`, and `google/gemini-2.5-pro`, plus a comparison run that keeps `openai/gpt-5.4-nano` as the current recommended relay model on speed/fit grounds.
  Docs impact: test_suite_behavior, relay_model_recommendation, version_number
- **Release narrative advanced to `1.3.0`.** Operator-facing docs and config examples now present `openai/gpt-5.4-nano` as the recommended relay model and frame the next planned publish as `1.3.0`, while preserving `1.2.21` and `1.2.22` as historical/prepared release waypoints.
  Docs impact: relay_model_recommendation, version_number

## [1.3.0] — 2026-04-20

### Security
- **REF-603 — plaintext bootstrap bundle JSON could leak in `/tmp` on failure.** `scripts/antenna-exchange.sh` now streams outbound bootstrap JSON directly from `jq` into `age` instead of writing a plaintext temp file first, and the import path installs cleanup traps immediately after decrypt so decrypted plaintext JSON is removed on normal return, validation failure, or signal interruption.
  Docs impact: bootstrap_bundle_handling
- **REF-400 — envelope-marker collisions could smuggle fake headers.** `scripts/antenna-relay.sh` now rejects any message whose body or sanitized header values contain `[ANTENNA_RELAY]` or `[/ANTENNA_RELAY]`, logging `status:MALFORMED (marker in body|headers)`. Sender (`antenna-send.sh`) also guards against injecting markers outbound.
- **REF-402 — no timestamp freshness check on inbound messages.** Relay now validates `timestamp:` against a freshness window (default: max 300s old, 60s future skew), configurable via `.security.max_message_age_seconds` / `.security.max_future_skew_seconds`. Rejected lines carry `nonce:` for correlation, consistent with REF-1501.
- **REF-403 (partial) — plaintext auth envelope persisted on receiver disk.** Relay temp files (`antenna-relay-exec.sh`, `antenna-relay-file.sh`) are now created under `umask 077`, `chmod 0600`'d, and `shred`'d-before-unlink on cleanup (best-effort, falls back to truncate+rm). The `/tmp/antenna-relay` parent dir is tightened to `0700` when owned. Full REF-403 (removing `auth:` from the wire) remains tracked alongside REF-402 HMAC work.
- **REF-404 — self-id fell back to `$(hostname)` if config was missing.** `antenna-send.sh` now fails fast with a clear error instead of silently using the machine hostname as a peer identity, preventing accidental cross-host identity collisions.
- **REF-501 — auth comparison was not constant-time.** Relay-side peer-secret comparison now uses a constant-time path to eliminate timing side-channels on secret verification.
- **REF-601 — expired bundle import succeeded silently.** `antenna-exchange.sh` import path now validates bundle expiry and refuses expired material with a clear error, covered by `tests/ref-601-expired-bundle-refusal.sh`.
- **REF-616 — exchange-bundle emails sent with bogus `antenna@localhost` From address.** `scripts/antenna-exchange.sh` no longer tries to read sender email from `himalaya account list -o json` (which never exposes `.email`) and no longer falls back to `antenna@localhost`. Sender email now resolves from the Himalaya TOML config at `${HIMALAYA_CONFIG:-${XDG_CONFIG_HOME:-$HOME/.config}/himalaya/config.toml}` via new helpers `himalaya_config_path` / `himalaya_account_email` / `himalaya_accounts_list`. Both `send_bundle_email` and `send_pubkey_email` hard-fail if the account's email cannot be resolved. Interactive flows no longer free-text-prompt for a Himalaya account name; they use selection-only confirmation through `confirm_from_account` (single-account hosts get a simple `Send? [Y/n]`; multi-account hosts get a numbered picker with strict numeric validation). `--account <name>` remains supported as strict selection of a configured account, not arbitrary sender editing. Regression: `tests/ref-616-himalaya-from-address.sh`.
  Docs impact: exchange_email_from_resolution

### Fixed
- **REF-300 / REF-303 — `antenna peers add` silently overwrote existing entries and null-ed out un-supplied fields.** `cmd_peers add` now refuses to touch an existing peer unless `--force` is given, and `--force` applies merge semantics: only fields explicitly supplied on the command line are overwritten, everything else (including unknown top-level fields like `.self` set by peer-exchange) is preserved. New-peer adds still require `--url` and `--token-file`; `--force` updates do not.
  Docs impact: peers_add_overwrite_policy, peer_registry_merge_semantics
- **REF-604 — `ensure_peer_entry_updated()` lost unknown peer-entry fields:** jq merge switched from `+` to `*` so nested peer fields (including `.self`) are preserved additively during peer updates.
  Docs impact: peer_registry_merge_semantics
- **REF-605 — legacy identity-secret export could leak over non-TTY stdout:** `legacy_export_runtime_secret()` now refuses to print the runtime identity secret when stdout is not a TTY and points operators at Layer A encrypted bootstrap instead.
  Docs impact: identity_secret_handling
- **REF-901 — setup could silently overwrite gateway `hooks.token`:** `scripts/antenna-setup.sh` now preserves an existing gateway `hooks.token` and only writes from Antenna's token file when the gateway value is absent or already matches.
  Docs impact: gateway_hooks_token_setup
- **REF-903 — setup reruns silently stripped operator `tools.exec` policy from the antenna agent:** the existing-agent repair path in `scripts/antenna-setup.sh` no longer does `del(.exec)`, so expert `tools.exec` overrides survive reruns. Setup still forces `sandbox.mode = "off"` and seeds the default deny list only when `tools.deny` is absent.
  Docs impact: setup_agent_update_behavior
- **REF-1206c — pair wizard no longer falsely implies bootstrap email delivery succeeded.** `scripts/antenna-pair.sh` now checks the real exit status from `antenna peers exchange initiate ... --send-email`, treats non-zero send attempts as failures, tells the operator the bundle was not sent, and falls back to explicit manual-delivery acknowledgement instead of fake-success wording.
  Docs impact: pair_wizard_email_delivery_behavior
- **REF-1501 — poll-loop couldn't fast-fail on auth/peer/rate-limit REJECTED:** `scripts/antenna-relay.sh` now tags all post-body REJECTED log lines with `nonce:$NONCE` (missing `from`, peer not in allowlist, unknown peer, missing/invalid peer secret, per-peer rate limit, global rate limit). The two pre-body envelope-marker MALFORMED paths intentionally remain nonce-less. Combined with REF-1502, `antenna test <model>` now exits on the first nonce-scoped REJECTED instead of waiting for `--timeout`.
  Docs impact: model_test_behavior
- **REF-1502 — `TEST_NONCE` generated but not used for log correlation:** `scripts/antenna-model-test.sh` now polls for nonce-scoped PASS (`INBOUND.*nonce:$TEST_NONCE.*status:relayed`) and nonce-scoped REJECTED instead of session-only matching, so concurrent runs can't cross-poison each other's results.
  Docs impact: model_test_behavior
- **REF-1504 — model-test swap bypassed gateway sync:** `scripts/antenna-model-test.sh` now swaps and restores `relay_agent_model` through `antenna config set ... --no-restart` (which also updates the antenna agent's `.model` in `openclaw.json`). Gateway is bounced exactly once after the initial swap and once in the cleanup trap, instead of per-run.
  Docs impact: model_test_behavior

### Added
- **`--no-restart` flag on `antenna config set` and `antenna model set`** for rapid-batch callers that want to write gateway config now and restart the gateway once at the end. Internal helper `_sync_relay_model_to_gateway` split into `_write_relay_model_to_gateway_config` (no restart) and `_restart_gateway`.
  Docs impact: model_test_behavior

### Docs
- README version/status refreshed for the prepared `v1.3.0` release, SKILL metadata includes canonical repository/homepage URLs for provenance, and operator-facing docs/config examples now present `openai/gpt-5.4-nano` as the recommended relay model.
  Docs impact: version_number, relay_model_recommendation

## [1.2.22] — 2026-04-20

### Note
- Historical/prepared release waypoint retained for continuity. Its substantive fixes were rolled into the prepared `1.3.0` release narrative above.

## [1.2.21] — 2026-04-18

### Fixed
- **Session resolution: sender no longer injects its own default session into outbound envelopes.** When `--session` is omitted, `target_session` is omitted from the envelope entirely; the recipient resolves from their own `default_target_session` config. Sender no longer needs to know the recipient's internal session layout. (Issue #17)
  Docs impact: session_resolution, version_number

### Docs
- README, SKILL.md, User Guide, and relay protocol docs were refreshed to reflect the session-resolution fix and align versioned operator-facing surfaces for the `1.2.21` publish.
  Docs impact: version_number, session_resolution

## [1.2.20] — 2026-04-17

### Fixed
- **Relay temp-file concurrency hazard:** the relay agent now uses unique temp files under `/tmp/antenna-relay/` instead of a shared fixed path, preventing message races under concurrent inbound traffic.
- **Inbox and rate-limit transaction races:** inbox queue mutations and inbound rate-limit state updates are now guarded with `flock`, preventing duplicate refs, lost queue entries, and weakened rate-limit enforcement.
- **Peer registry drift poisoning:** peer-reading/status/doctor/test/send surfaces now ignore malformed top-level entries and only treat real peer objects with string `url` fields as peers.
- **Regression-suite drift:** Tier A/B/C tests now match the live relay contract, full-session-key behavior, and locking expectations.
- **Release-surface version drift:** SKILL metadata, guide versioning, and validation docs now align on `1.2.20`.

### Changed
- **Validation and review artifacts added:** Phase 1 review and validation checklists are now tracked in `references/` to preserve the Apr 17 hardening audit trail.
- **Docs refreshed to current relay reality:** current file-based relay flow, full session keys, and known superseded guidance are reflected across operator-facing docs.

### Fixed (post-release)
- **Session resolution: sender no longer injects its own default session into outbound envelopes.** When `--session` is omitted, `target_session` is omitted from the envelope entirely; the recipient resolves from their own `default_target_session` config. Sender no longer needs to know the recipient's internal session layout. (Issue #17)
  Docs impact: session_resolution, version_number

### Known issue
- **Hook relay session may report `sessions_send` timeout even when delivery succeeds.** Cross-host smoke on 2026-04-17 confirmed successful end-to-end delivery despite the relay session showing a timeout in Control UI. Treat this as an operational/UI timing quirk, not a transport failure.

## [1.2.19] — 2026-04-13

### Added
- **`antenna sessions` subcommand** — CLI management of `allowed_inbound_sessions`:
  - `antenna sessions list` — show current allowed inbound session targets
  - `antenna sessions add <name> [<name>...]` — add session target(s) with duplicate detection
  - `antenna sessions remove <name> [<name>...]` — remove session target(s) with core-session protection (`main`/`antenna` require `--force`)
  - Batch add/remove supported; counters for added/skipped/removed/blocked

### Changed
- **Full session keys everywhere** — all session references use full keys (`agent:betty:main` instead of `main`). Config fields `default_target_session` and `allowed_inbound_sessions` both store full keys. Setup generates them from `local_agent_id`. No expansion in the relay — bare names are rejected.
- Relay allowlist validation simplified to exact-match only (removed prefix, segment matching, and bare-name expansion)
- CLI `sessions add/remove` auto-expands bare names to full keys for convenience, with visible `→ Expanded` feedback
- `antenna-send.sh` `--session` flag now expects full session keys

### Docs impact
SKILL.md (session allowlist section rewritten for full-key convention, config example updated, version bump to 1.2.19), CHANGELOG.md, USER-GUIDE.md (envelope example, local_agent_id description, troubleshooting), antenna-config.example.json, antenna-send.sh help text.

**Note:** FSD (`ANTENNA-RELAY-FSD.md`) still references bare `main` shorthand and old matching semantics in several places. Deferred to a dedicated FSD revision pass.

## [1.2.18] — 2026-04-13

### Fixed
- **Docs: removed stale `commands.ownerDisplay` requirement** — confirmed not needed for relay delivery or Control UI visibility; was cargo-cult from restart timing
- **Docs: removed stale `tools.exec` override guidance** — explicit `tools.exec.security`/`tools.exec.ask` on the Antenna agent causes silent relay failure (see v1.2.14); all docs now warn against setting these
- **Docs: corrected trust-model claims** — ClawReef stores `hooksToken` and `identitySecret` for push delivery; replaced false "only public metadata" / "never bilateral secrets" copy with honest webhook-provider framing
- **Docs: fixed install command** — remaining `bash skills/antenna/install.sh` references updated to `bash skills/antenna/bin/antenna.sh setup`
- **Docs: updated GitHub URLs** — `cshirley001/openclaw-skill-antenna` → `ClawReefAntenna/antenna` across User Guide and static site
- **Setup script: removed `ownerDisplay` config step** — setup no longer sets `commands.ownerDisplay = "raw"`; renumbered remaining steps
- **Docs: documented actual config requirements** — `tools.sessions.visibility = "all"`, `tools.agentToAgent.enabled = true`, and `sandbox: { mode: "off" }` are the real requirements for relay operation

### Docs impact
README, SKILL.md, User Guide, setup script summary output, static site (index.html, user-guide.html)

## [1.2.17] — 2026-04-12
### Fixed
- Pair wizard once again offers to email bootstrap bundles after creating them, using the existing exchange mail flow
- Wizard now behaves gracefully on hosts without `gog` or `himalaya` by simply not offering the email option

## [1.2.16] — 2026-04-12
### Fixed
- Setup now includes `workspace` when creating default main agent entry — missing workspace caused hook-injected relay messages to be invisible in Control UI
- Uses user-provided `--agent-id` (not hardcoded `lobster`) for the default agent

## [1.2.15] — 2026-04-12
### Fixed
- Setup no longer hardcodes `lobster` as default main agent ID when `agents.list` is empty — now uses the user-provided `--agent-id` value, so relay messages target the correct registered agent
- Non-interactive setup auto-detects primary agent from gateway config when `--agent-id` is omitted, and warns/corrects if the supplied ID doesn't match a registered agent
- Updated help text examples to use `main` instead of `lobster`

## [1.2.14] — 2026-04-12

### Fixed
- **Relay agent exec policy:** Setup no longer sets `tools.exec.security` or `tools.exec.ask` on the antenna agent registration. Explicit exec overrides caused silent relay failures where the hook session acknowledged messages but `sessions_send` never executed, making relayed messages invisible in the Control UI despite successful delivery. The relay now inherits the default exec policy, matching the proven working configuration.

### Changed
- Existing antenna agent entries are updated on re-run to remove stale `tools.exec` overrides.
- Setup summary output no longer shows exec allowlist settings.

## [1.2.13] — 2026-04-12

### Fixed
- **Relative token path resolution:** `peers test`, `antenna-send.sh`, and `antenna-health.sh` now resolve relative `token_file` paths against the skill directory. Previously, these commands silently sent an empty Bearer token when invoked from a different working directory, causing `401 AUTH FAILED` despite correct credentials.

## [1.2.12] — 2026-04-12

### Fixed
- **Fresh-install setup guard:** running `antenna` before setup now prints a clear next-step hint instead of failing on missing runtime files.
- **`set -e` second-run crash:** the self-healing permissions pass in `bin/antenna.sh` no longer exits the script when there are no permissions left to fix.

### Changed
- **Zero-config onboarding hint:** unconfigured installs now direct the user to `antenna setup` or `bash skills/antenna/bin/antenna.sh setup`.

## [1.2.9] — 2026-04-12

### Changed
- **Self-healing permissions:** `antenna.sh` now auto-fixes execute bits on all scripts on first run. `install.sh` is no longer required after `clawhub install`. The new onboarding flow is just: `clawhub install antenna && bash skills/antenna/bin/antenna.sh setup`.
- **Simplified Quick Start:** README and User Guide consolidated install + setup into a single two-command step. `install.sh` remains available but is marked optional.

## [1.2.8] — 2026-04-12

### Fixed
- **Pairing wizard crash on clean install:** `scripts/antenna-pair.sh` hard-coded `bin/antenna` instead of the renamed `bin/antenna.sh` entrypoint, causing immediate failure.
- **Dangling CLI symlink after uninstall:** `antenna uninstall --purge-skill-dir` now removes the `/usr/local/bin/antenna` (or `~/.local/bin/antenna`) symlink created by setup, instead of leaving it dangling.

## [1.2.7] — 2026-04-11

### Added
- **Support contact info** (`help@clawreef.io`) added to README, SKILL.md, User Guide, `install.sh`, and `antenna doctor` output.
- **"Getting Help" section** in README with email, GitHub Issues, ClawReef, and SECURITY.md links.
- **SECURITY.md** for responsible vulnerability disclosure (standard GitHub convention).
- `antenna doctor` now prints support contact info when warnings or failures are present.
- `install.sh` now shows support contact info at the end of every run.

## [1.2.6] — 2026-04-11

### Added
- **`install.sh` post-install bootstrap script.** Fixes file permissions (ClawHub doesn't preserve execute bits on `.sh` files) and offers to run `antenna setup`. New user flow: `clawhub install antenna && bash skills/antenna/install.sh`.
- Updated README and User Guide install instructions to include the `install.sh` step.

## [1.2.5] — 2026-04-11

### Fixed
- **ClawHub packaging fix:** Renamed `bin/antenna` → `bin/antenna.sh` so the CLI dispatcher is included in ClawHub packages. ClawHub's `listTextFiles()` silently drops extensionless files because they fail the text-extension allowlist check. The symlink created by `antenna setup` remains just `antenna` on PATH.
- Updated all internal references (setup symlink logic, file inventories, FSD, docs) to reflect the new `bin/antenna.sh` filename.

## [1.2.4] — 2026-04-10

### Fixed
- Setup agent auto-detection now handles both `agents.entries{}` and `agents.list[]` gateway config formats
- Pair wizard Step 3 now hints to choose [S]kip for email/manual exchange when not using ClawReef
- Pair wizard Steps 4+ show a "skip 4–6" note when ClawReef invite was used in Step 3

## [1.2.3] — 2026-04-10

### Added
- **ClawReef integration** — ClawReef peer registry references throughout docs (README, SKILL.md, User Guide)
- **Setup**: ClawReef info block displayed after setup completion with registration guidance
- **Pair wizard**: New Step 3 "Send a ClawReef invite" offers registry-based discovery as alternative to manual encrypted exchange; opens browser to invites page if desired
- User Guide: Full "ClawReef — The Reef Directory" section explaining purpose, trust model, and how it fits into pairing
- README: ClawReef section with overview, trust model, and usage
- SKILL.md: ClawReef peer discovery section

### Changed
- Pair wizard expanded from 7 to 8 steps (ClawReef invite inserted as Step 3; existing steps renumbered)
- Roadmap entries updated to reflect ClawReef is now live

## [1.2.0] — 2026-04-09

### Changed
- **Playful voice pass** for `antenna setup` and `antenna pair` — user-facing copy
  rewritten with warm, confident tone inspired by the Antenna-for-OpenClaw doc.
- Setup banner: "Let's Get You on the Reef" with two-minute promise and shellfish joke.
- Step headers gain warm subtitles (e.g. "Who Are You on the Reef?", "Choosing Your Dispatcher").
- Relay model hint: "a courier, not a philosopher."
- Inbox description: "Like a walkie-talkie" / "Trusted peers can skip the line."
- Completion: "Welcome to the reef, <host>. 🦞"
- Pair wizard intro: "Let's connect you to another host on the reef."
- Pair completion: "🦞 You're Claw-nected!" / "The ocean just got smaller."
- First message send: "Releasing the lobster to <peer>... 🦞"
- Error messages gain human warmth while staying clear.
- Quit message: "No worries — pick up where you left off anytime."
- Total pun count across both scripts: 2. Emoji 🦞 count: 6.

## [1.1.9] — 2026-04-09

### Added
- **Interactive peer pairing wizard:** New `antenna pair` command walks users through the full
  pairing flow — keypair generation, public key sharing, bundle creation, bundle import,
  connectivity test, and first message — with Next/Skip/Quit at each step.
- `scripts/antenna-pair.sh` — standalone wizard script.
- `antenna pair [--peer-id <id>]` — CLI entry point.
- Auto-offered at the end of `antenna setup` (interactive mode only).

### Changed
- `antenna setup` end-of-run output now shows a concise pairing summary with an offer to
  launch the wizard, replacing the previous static step-by-step listing.

## [1.1.8] — 2026-04-09

### Changed
- **File-based relay input (eliminates model encoding dependency):** The relay agent no longer
  performs base64 encoding. Instead, it uses the `write` tool to save the raw inbound message
  to a temporary file, then execs `antenna-relay-file.sh` with the file path as the sole
  argument. At v1.1.8 this used a fixed temp path; later hardening superseded that with unique
  per-message temp files under `/tmp/antenna-relay/`. The script reads the file and pipes it to
  `antenna-relay.sh --stdin`. This removes the entire class of model-dependent encoding failures
  — notably `gpt-5.4` refused to base64-encode large payloads under the v1.1.6 approach.
- Updated `agent/AGENTS.md` with the new write-then-exec flow and simplified instructions.
- Supersedes `antenna-relay-exec.sh` (base64 wrapper) as the primary relay entry point.

### Added
- `scripts/antenna-relay-file.sh` — reads raw message from a file and feeds to relay via stdin.

## [1.1.7] — 2026-04-09

### Fixed
- **`local` keyword outside function:** Fixed `scripts/antenna-relay.sh` line 229 where
  `local auth_hint expected_hint diag_msg` was used at top-level script scope (outside any
  function). This caused `local: can only be used in a function` errors on the peer-auth
  mismatch diagnostic path. Replaced with plain variable assignments. Bug was latent on hosts
  where auth always succeeded; only surfaced on AntTest where peer-secret mismatches triggered
  the affected branch.

## [1.1.6] — 2026-04-07

### Changed
- **Base64-encoded relay exec argument:** The relay agent now base64-encodes the full raw
  inbound message before passing it to `antenna-relay-exec.sh`. The wrapper decodes before
  piping to the relay script. This eliminates the entire class of exec allowlist failures
  caused by message content containing shell metacharacters (`|`, `&`, `;`, `$`, etc.).
- Updated `agent/AGENTS.md` with base64 encoding instructions and examples.

## [1.1.5] — 2026-04-06

### Changed
- **Lean skill package:** Split docs into two tiers for distribution clarity:
  - `references/` (ships with skill): `ANTENNA-RELAY-FSD.md`, `issues.md` — files the agent may load during work
  - `docs/` (repo-only, operator/historical): security assessment, red team report, removal checklist, design-history docs
- Updated file inventory in SKILL.md and fixed cross-references in CHANGELOG.md.

## [1.1.4] — 2026-04-06

### Changed
- **Directory convention:** Renamed `docs/` → `references/` to align with AgentSkills spec (`scripts/`, `references/`, `assets/` canonical layout). All internal cross-references updated.
- `agent/` and `bin/` retained as-is — these are infrastructure-skill necessities with no spec equivalent.

## [1.1.3] — 2026-04-06

### Fixed
- **SKILL.md frontmatter compliance:** Removed non-standard `version` key (moved to `metadata.version`); replaced angle brackets in description with uppercase placeholders. Now passes AgentSkills `quick_validate.py` cleanly.
- **Trigger coverage:** Added "check antenna inbox" and "approve message" to description triggers.

## [1.1.2] — 2026-04-06

### Added
- **CLI PATH symlink:** `antenna setup` now automatically symlinks `bin/antenna` into a PATH directory (`/usr/local/bin` or `~/.local/bin`), so agents and humans can run `antenna` directly without knowing the skill install path. Falls back to manual instructions if symlink cannot be created.

## [1.1.1] — 2026-04-06

### Fixed
- **Setup Step 5 display:** `echo` → `echo -e` for ANSI bold/color codes in the inbox mode description
- **Agent ID auto-detection:** Setup now reads gateway config to pre-fill the primary agent ID, reducing the chance of entering the wrong value and getting misrouted sessions (e.g., `agent:lobster:main` vs `agent:main:main`)
- **Cross-agent session visibility:** Setup now auto-configures `tools.sessions.visibility=all` and `tools.agentToAgent.enabled=true` in the gateway config, fixing "Session send visibility is restricted" errors on fresh installs
- **Manual fallback instructions** updated with the new visibility/agent-to-agent settings (Step 4) and renumbered

## [1.1.0] — 2026-04-06

### Summary
Inbox: optional approval queue for inbound messages. Directly addresses the two HIGH severity security findings (SEC-1, SEC-2) from the v1.0.20 security assessment by making sandbox-off + silent exec optional rather than required.

### Added
- **Inbox approval queue** (`scripts/antenna-inbox.sh`): When `inbox_enabled` is `true`, inbound messages from non-auto-approved peers are queued for operator review instead of being relayed immediately.
- **Auto-approve peer list** (`inbox_auto_approve_peers` in config): Trusted peers bypass the queue and relay instantly. Provides progressive trust — new peers start in the queue, graduate to auto-approve once trusted.
- **CLI commands:**
  - `antenna inbox` / `antenna inbox list` — table view of pending messages (Ref#, Time, From, To, Preview)
  - `antenna inbox count` — pending count (for heartbeat/cron integration)
  - `antenna inbox show <ref>` — full message body
  - `antenna inbox approve all|<refs>` — selective approval with comma-separated refs and ranges (e.g., `1,3,5-7`)
  - `antenna inbox deny all|<refs>` — selective denial
  - `antenna inbox drain` — outputs JSON delivery instructions for approved items; calling agent delivers via `sessions_send`
  - `antenna inbox clear` — purge processed items
- **Internal `queue-add` command** for `antenna-relay.sh` to add validated messages to the queue.
- **Relay agent `queue` response**: Agent now handles `{"action":"queue"}` script output and replies `Queued: ref #N from <peer>`.

### Changed
- `antenna-relay.sh` — new inbox branch after all validation passes (peer auth, rate limiting, message length). When inbox is enabled, non-auto-approved peers' messages are fully validated then queued. Auto-approved peers and inbox-disabled mode fall through to the existing immediate relay path.
- `antenna-config.example.json` — three new fields: `inbox_enabled`, `inbox_auto_approve_peers`, `inbox_queue_path`.
- `scripts/antenna-setup.sh` — generates inbox config defaults (disabled by default).
- `bin/antenna` — `inbox` subcommand wired with help text.
- `agent/AGENTS.md` — queue response handling added to relay agent instructions.

### Design Decisions
- **Drain outputs JSON, does not self-deliver.** `antenna inbox drain` outputs `{"action":"deliver","sessionKey":"...","message":"..."}` lines to stdout. The calling agent (primary assistant or cron) reads these and calls `sessions_send`. This avoids re-entering the relay agent via `/hooks/agent` which could re-queue the message.
- **Message format is identical.** The relay script builds the complete formatted message (📡 header, security notice, body) *before* the queue decision. Approved messages arrive in the target session looking exactly the same as direct-relay messages.
- **Backwards compatible.** `inbox_enabled: false` (the default) preserves all existing behavior. No changes to the immediate relay path.
- **Inbox reduces relay agent permissions.** With inbox enabled, the relay agent only needs `exec` (to run the relay script that queues). It no longer needs `sessions_send` for queued peers, since delivery moves to the drain caller.

### Security Impact
- Operators who enable inbox mode can optionally run the relay agent with stricter security, since the relay agent no longer delivers directly for queued peers.
- Auto-approve provides tiered trust without all-or-nothing security decisions.
- Queue file has the same exposure profile as the existing antenna.log.

## [1.0.20] — 2026-04-06
### Added
- **Heredoc-free relay wrapper (`antenna-relay-exec.sh`):** New wrapper script that accepts the raw message as `$1`, writes it to a temp file, and pipes to `antenna-relay.sh --stdin`. Avoids all dynamic shell constructs in the exec call.
- **Per-agent exec policy:** Setup now configures `tools.exec.security = "allowlist"` and `tools.exec.ask = "off"` on the antenna agent.

### Changed
- **Relay agent instructions (`agent/AGENTS.md`):** Fully rewritten for allowlist compatibility. The exec command is now a single simple invocation: `bash ../scripts/antenna-relay-exec.sh '<message>'` — no config lookup, no `$(...)`, no chaining. Explicit prohibition on heredocs, here-strings, command substitution, semicolons, `&&`, `||`, and backticks added to agent rules.
- **Setup manual instructions:** Updated to include `tools.exec.security: allowlist` and `tools.exec.ask: off` in the agent registration block.

### Fixed
- **Root cause of persistent exec approvals (CONFIRMED):** OpenClaw's allowlist evaluator flags two classes of dynamic shell constructs — `requiresHeredocApproval` (triggered by `<<` tokens) and inline eval/command substitution (triggered by `$(...)` and backticks). The v1.0.19 relay instructions eliminated heredocs but still used `$(jq -r '.install_path' ...)` for config lookup, which continued to trip allowlist denial. Fixed by removing ALL dynamic constructs: the agent now calls the wrapper via relative path (`../scripts/`) with no config resolution in the exec command itself. The wrapper handles path resolution internally via `SCRIPT_DIR`.
- **Confirmed working:** Tests 11 and 12 on AntTest (clean Ubuntu 24.04 WSL2 environment) both delivered without any approval prompt or exec denial.

## [1.0.19] — 2026-04-06
### Added
- **Control UI visibility:** Setup now sets `commands.ownerDisplay = "raw"` in gateway config. Without this, hook-delivered messages (including Antenna relays) are processed and delivered but invisible in the Control UI chat view. This was the root cause of the long-standing "messages not showing up" issue.
- **Least-privilege agent registration:** Antenna agent is now registered with `sandbox: { mode: "off" }` and a restrictive `tools.deny` list. The tools.deny list blocks web, browser, image, cron, and memory tools — the relay only needs `exec` and `sessions_send`.

## [1.0.18] — 2026-04-03
### Added
- Interactive email prompt after bundle creation: when running `initiate` or `reply` interactively with gog or himalaya available, the wizard now offers to email the bundle directly — no `--send-email` flag needed.
- Multi-method email send: tries `gog` (Gmail API with native `--attach`) first, falls back to `himalaya` (raw MIME via stdin), fails clearly if neither is available.

### Fixed
- `--send-email` crash: himalaya's mail-parser panicked when raw MIME was passed as a CLI argument; switched to stdin pipe.
- Missing `From:` header in himalaya MIME path caused "cannot send message without a sender" error.

## [1.0.17] — 2026-04-03
### Fixed
- `send_bundle_email()` rewritten to use raw MIME with base64-encoded attachment instead of MML (which crashed himalaya's mail-parser).
- Added gog as primary email send method with himalaya as fallback.

## [1.0.16] — 2026-04-03
### Added
- `antenna model show` / `antenna model set <model>` — convenience commands for relay model management.
- `antenna config set relay_agent_model` now syncs the model to the gateway config (`~/.openclaw/openclaw.json`) and restarts the gateway automatically.
- Setup wizard Step 4/6 now reads model aliases from the user's gateway config and presents a numbered picker during interactive install.
- Non-interactive `--model` flag also resolves alias names to full provider/model IDs.

### Changed
- Default relay model changed from `openai/gpt-5.4` to `openai/gpt-5.4-nano-2026-03-17` (cheaper, more mechanical — better suited for relay duty).
- Updated all example/help text to reflect the new default.

## [1.0.15] — 2026-04-03
### Added
- New `antenna uninstall` command for conservative cleanup/removal of Antenna installs.

### Changed
- Began separating **tracked reference config** from **live local runtime config**.
- Added `antenna-config.example.json` and `antenna-peers.example.json` as shareable reference templates.
- Marked `antenna-config.json` and `antenna-peers.json` as local runtime files to be generated by `antenna setup` and kept out of git history.
- Updated setup/docs to point operators toward `antenna setup` for live config generation and `*.example.json` for reference/manual recovery.

### Notes
- `antenna uninstall` removes Antenna runtime files, logs, test artifacts, Antenna-owned secrets, and Antenna gateway registration entries by default, while leaving the rest of OpenClaw alone.
- `--purge-skill-dir` is available for true full removal after cleanup.

## [1.0.11] — 2026-04-03

### Summary
Onboarding hardening: seven rough edges from real first-run experience smoothed out.

### Added
- **Token autodiscovery** in `antenna setup`: reads `hooks.token` from `~/.openclaw/openclaw.json` and offers to create the token file automatically (Item #2).
- **Automatic gateway registration** in `antenna setup`: merges hooks config and registers the Antenna agent entry directly into the gateway JSON, with backup-before-edit and JSON validation. Falls back to manual instructions if user declines or gateway config is not found (Item #3).
- **Schema-aware agent registration**: agent entries omit `systemPrompt` to avoid schema rejection on OpenClaw builds that don't support it inline; uses `agentDir` (not `agentsDir`) to match observed live config schema (Item #4).
- **Interactive `age` installer** in `antenna peers exchange`: when `age` is missing, offers to install via Homebrew; if install fails or is declined, offers legacy fallback interactively instead of hard-failing (Item #5).
- **`peers add` allowlist prompt**: after adding a peer, prompts "Add to inbound/outbound allowlists?" (default: yes). Non-interactive mode auto-adds. Prevents the "not in allowed_outbound_peers" surprise (Item #6).
- **Enhanced auth mismatch diagnostics** in `antenna-relay.sh`: on invalid peer secret, logs prefix/suffix hints of received vs expected values and suggests `antenna peers exchange` resync — without exposing full secrets (Item #7).

### Changed
- `antenna setup` gateway registration section now prints manual instructions only when auto-registration was declined or unavailable.
- `antenna setup` next-steps block adapts based on whether auto-registration succeeded.

### Fixed
- Gateway registration no longer includes `systemPrompt` field that some OpenClaw builds reject (Item #4).

## [1.0.10] — 2026-04-01

### Summary
Layer A encrypted bootstrap exchange implemented and docs synced to the current transport/trust model.

### Added
- **Layer A encrypted bootstrap exchange** in `scripts/antenna-exchange.sh` using `age` armored bundles.
- New exchange commands:
  - `antenna peers exchange keygen`
  - `antenna peers exchange pubkey`
  - `antenna peers exchange initiate <peer-id>`
  - `antenna peers exchange import [file|-]`
  - `antenna peers exchange reply <peer-id>`
- **Import preview + confirmation** before applying allowlist changes.
- **Peer registry support for `exchange_public_key`**.
- **Optional Himalaya direct-send convenience** for bootstrap bundles.

### Changed
- `scripts/antenna-exchange.sh` rewritten from the older raw-secret wizard into a dispatcher that supports encrypted bundle exchange plus explicit legacy fallback.
- `bin/antenna` help text updated for the new exchange flow and peer-add support for `--exchange-public-key`.
- `antenna status` now reports local Layer A key presence and warns when peers lack exchange public keys.
- `references/ANTENNA-RELAY-FSD.md` and `SKILL.md` updated to reflect:
  - reachable HTTPS peer model,
  - layered trust (`url` + hook token + per-peer identity secret),
  - Layer A encrypted onboarding,
  - current config and peer-registry fields.

### Fixed
- `scripts/antenna-exchange.sh` key generation path no longer uses a pre-created temporary file with `age-keygen -o`, which caused `keygen` to fail during functional verification. It now generates inside a temporary directory with fresh output paths.

### Compatibility
- Legacy raw-secret commands remain available:
  - `antenna peers exchange <peer-id> --export`
  - `antenna peers exchange <peer-id> --import <file>`
  - `antenna peers exchange <peer-id> --import-value <hex>`

### Notes
- Secure Layer A requires `age` / `age-keygen`.
- Himalaya is optional; email remains convenience transport only, not part of the trust model.

## [1.0.8] — 2026-03-30

### Summary
Onboarding UX fixes from first real "meat test" (human walkthrough on clean-slate host).

### Fixed
- **`antenna setup`** now seeds the host's own ID into `allowed_inbound_peers` and `allowed_outbound_peers` — prevents self-loopback smoke tests from failing with "not in allowed_outbound_peers" immediately after setup.
- **`antenna peers exchange` wizard** reordered secret-sharing options: **paste/import-value** is now Option A (easiest, always works); **pull from remote** is Option B (note that the *other* host's operator can grab the secret); **scp push** is now Option C (only shown when peer URL is known); **manual secure channel** is Option D. Previously SCP was listed first, which assumes bidirectional SSH access that doesn't always exist.

### Changed
- `scripts/antenna-setup.sh` — `allowed_inbound_peers` and `allowed_outbound_peers` now default to `[$host_id]` instead of `[]`.
- `scripts/antenna-exchange.sh` — reordered guided wizard Step 2 options; added "operator can pull" suggestion.

### Tested
- Clean-slate onboarding: `antenna setup` → `peers add` → `peers exchange` → `antenna msg` — full round-trip confirmed.
- Tier A: 11/11 on both hosts after changes.

## [1.0.7] — 2026-03-30

### Summary
Token file permission audit in `antenna status` and log value sanitization in the relay script.

### Added
- **Security audit in `antenna status`:** Checks file permissions on all peer token files, config file, and peers file. Warns if any are too permissive (token files should be 600; config/peers should be 644 or tighter). Also now displays rate limit config and session allowlist in the status output.
- **Log value sanitization:** All peer-supplied header values (`from`, `target_session`, `subject`, `user`, `timestamp`, `reply_to`) are now sanitized before logging and processing — control characters stripped, newlines removed, values truncated to safe maximum lengths. Prevents log injection and log forgery via crafted envelopes.
- **`sanitize_log_value` helper** in `antenna-relay.sh`: Strips `\n`, `\r`, `\t`, other control chars; collapses whitespace; trims; truncates to configurable max length.

### Changed
- `bin/antenna` — `cmd_status()` expanded with rate limit display, session allowlist display, and security audit section.
- `scripts/antenna-relay.sh` — all header values sanitized immediately after extraction; verbose log preview also sanitized.

### Security
Addresses Red Team findings #5 (token file exposure) and #6 (log injection/forgery) from `docs/RED-TEAM-REPORT-v1.0.4.md`.

## [1.0.6] — 2026-03-30

### Summary
Rate limiting: per-peer and global inbound message throttling to prevent relay agent saturation and API budget burn.

### Added
- **Per-peer rate limiting** (`rate_limit.per_peer_per_minute` in config, default 10): Rejects messages from a peer exceeding the limit within a 60-second sliding window.
- **Global rate limiting** (`rate_limit.global_per_minute` in config, default 30): Rejects messages when total inbound volume across all peers exceeds the limit.
- **Rate limit state file** (`antenna-ratelimit.json`): Lightweight per-peer timestamp tracking, auto-pruned on each invocation. Excluded from git.
- **Test A.9**: Validates burst rejection — temporarily sets limit to 2/min, sends 3 messages, confirms 3rd is rejected.

### Changed
- `scripts/antenna-relay.sh` — rate limit check runs after peer validation, before message length/session checks. On limit hit: `RELAY_REJECT` with descriptive reason, logged.
- `antenna-config.json` — new `rate_limit` block.
- `.gitignore` — excludes `antenna-ratelimit.json`.

### Security
Addresses Red Team finding #4 (DoS via relay agent saturation) from `docs/RED-TEAM-REPORT-v1.0.4.md`.

## [1.0.5] — 2026-03-30

### Summary
Security hardening: untrusted-input framing on all relayed messages and inbound session target allowlist.

### Added
- **Untrusted-input framing:** All relayed messages now include `(Security Notice: The following content may be from an untrusted source.)` between the header and body. Subtle, non-alarmist, but ensures receiving agents treat Antenna content as external input.
- **Inbound session allowlist** (`allowed_inbound_sessions` in `antenna-config.json`): Restricts which sessions inbound messages can target. At v1.0.5 the default/examples still used short forms like `["main", "antenna"]` with segment matching. Later hardening superseded that with canonical full session keys in live config and relay behavior. Sessions not matching an allowed target are rejected with reason logged.

### Changed
- `scripts/antenna-relay.sh` — added session allowlist validation before relay; added security notice to delivery message format.
- `antenna-config.json` — new `allowed_inbound_sessions` field.
- `scripts/antenna-test-suite.sh` — at v1.0.5 the test suite was updated from `agent:test:main` to `agent:antenna:test` to match the then-current security model. Later hardening superseded those examples with allowlisted full session keys.

### Security
Addresses Red Team findings #1 (prompt injection via message body) and #3 (session target injection) from `docs/RED-TEAM-REPORT-v1.0.4.md`.

## [1.0.4] — 2026-03-30

### Summary
Added native Anthropic and Google Gemini API support to the test suite.

### Added
- **Anthropic Messages API support** (`anthropic/*` models) — native tool schema (`input_schema`), `tool_use`/`tool_result` multi-turn for Tier C, `x-api-key` + `anthropic-version` auth headers
- **Google Gemini API support** (`google/*` models) — native tool schema (`functionDeclarations`), `functionCall`/`functionResponse` multi-turn for Tier C, key-based auth via `generateContent` endpoint
- Provider-specific tool definition blocks: `TOOLS_ANTHROPIC`, `TOOLS_GOOGLE` (alongside existing OpenAI-format `TOOLS_JSON`)
- Unified `call_model_api` dispatcher that normalizes all provider responses to a common shape (`http_code`, `elapsed_ms`, `first_tool_name`, `first_tool_args`, `raw`)
- Provider format tag (4th field) in `resolve_model_api` output: `openai`, `anthropic`, or `google`

### Changed
- `run_tier_b()` and `run_tier_c()` rewritten to use unified dispatcher — provider-agnostic assertions
- `check_model_api()` updated to parse 4-field pipe format

### Tested
- `anthropic/claude-sonnet-4-20250514`: 8/8 suite, live smoke PASS (9.3s)
- `google/gemini-2.5-flash`: 8/8 suite, live smoke PASS (~2min — arrives correctly but the hook→agent pipeline is slower; use `--timeout 90`+ for live smoke tests with Gemini)

### Supported providers (Tier B/C) — now 7 families
- OpenAI (`openai/*`)
- OpenAI Codex (`openai-codex/*`)
- OpenRouter (`openrouter/*`)
- Nvidia NIM (`nvidia/*`)
- Ollama (`ollama/*`)
- **Anthropic** (`anthropic/*`) — NEW
- **Google Gemini** (`google/*`) — NEW

## [1.0.3] — 2026-03-30

### Summary
Enriched test messages with meaningful metadata for forensic traceability.

### Changed
- `scripts/antenna-model-test.sh` — live smoke test messages now include: model name, run number, unique nonce, hostname, timestamp, and timeout value (replaces generic "antenna-model-test run N" string)
- `scripts/antenna-test-suite.sh` — Tier B and Tier C test envelopes now include: tier label, model under test, hostname, and test timestamp (replaces static "Hello from the model tester" body)
- Tier C simulated relay output reflects enriched content for consistent C.4 validation
- C.4 assertion updated to match new message content patterns

### Why
Test messages that carry context about what produced them make relay debugging and multi-model comparison forensically useful — you can trace any delivered message back to the exact model, tier, and timestamp that generated it.

## [1.0.2] — 2026-03-30

### Summary
Three-tier test suite with multi-model comparison, structured reports, and multiple output formats.

### Added
- `scripts/antenna-test-suite.sh` — decomposed tester with three evaluation tiers:
  - **Tier A:** deterministic script validation (8 tests) — feeds envelopes into `antenna-relay.sh`, checks JSON output with `jq`. No model, no network.
  - **Tier B:** model → exec tool call (4 tests) — direct provider API call, verifies model emits correct `exec` invocation referencing relay script with envelope.
  - **Tier C:** model → sessions_send (4 tests) — simulated relay response, verifies model emits correct `sessions_send` with matching sessionKey and message.
- Multi-model comparison via `--models "a,b,c"` (max 6) with side-by-side table, scores, timing, and verdict
- `--report [dir]` saves structured output: `summary.md`, `summary.json`, `tier-a.json`, and per-model `tier-b-request.json`, `tier-b-response.json`, `tier-c-request.json`, `tier-c-response.json`
- `--format terminal|markdown|json` output formats
- `--verbose` inline request/response payloads
- CLI wiring: `antenna test-suite [options]`
- `.gitignore` updated to exclude `test-results/`

### Supported providers (Tier B/C) at time of release
- OpenAI (`openai/*`)
- OpenAI Codex (`openai-codex/*`)
- OpenRouter (`openrouter/*`)
- Nvidia NIM (`nvidia/*`)
- Ollama (`ollama/*` — local models)
- (Anthropic and Google added in v1.0.4)

### Note
The existing `antenna test` self-loop integration tester remains available as a smoke/end-to-end test. The new `antenna test-suite` is the primary model compatibility evaluator.

## [1.0.1] — 2026-03-29

### Summary
Portability cleanup. Removed hardcoded host/user/model assumptions from shareable docs and agent files. All host-specific settings now live exclusively in config files.

### Changed
- `relay_agent_model` reverted from `"mini"` alias to full `"openai/gpt-5.4"` provider/model ID
- `agent/AGENTS.md` — replaced hardcoded `/home/corey/clawd/...` paths with relative/config-driven resolution
- `agent/TOOLS.md` — same path portability fix
- `SKILL.md` — generic `<placeholder>` examples instead of installation-specific names and URLs
- `README.md` — same generic examples treatment
- `references/ANTENNA-RELAY-FSD.md` — removed host-specific peer IDs, session keys, and display names from examples
- `bin/antenna` — generic usage examples; status fallback model shows `"unset"` instead of `"mini"`
- `scripts/antenna-relay.sh` — fallback `local_agent_id` changed from example agent to `"agent"`

### Added
- `install_path` field in `antenna-config.json` — allows agent/scripts to resolve paths on any host

### Portability principle
Config files (`antenna-config.json`, `antenna-peers.json`) hold all host-specific state. Docs and agent files use generic placeholders. New installations edit config, not code.

## [1.0.0] — 2026-03-29

### Summary
First stable release. Script-first relay architecture with dedicated lightweight agent, full CLI, peer management, and transaction logging.

### Added
- `antenna-send.sh` — builds `[ANTENNA_RELAY]` envelope and POSTs to peer `/hooks/agent`
- `antenna-relay.sh` — deterministic parsing, validation, formatting, and logging on the receiving end
- `antenna-health.sh` — peer health check via `/health` endpoint
- `antenna-peers.sh` — list known peers from registry
- `bin/antenna` — CLI dispatcher (`send`, `msg`, `peers`, `config`, `log`, `status`)
- `antenna-config.json` — system configuration (max message length, allowed peers, logging, MCS toggle)
- `antenna-peers.json` — flat peer registry with URL, token file, display name, self flag
- `agent/AGENTS.md` — dedicated Antenna relay agent instructions
- `agent/TOOLS.md` — agent tool reference (relay script paths)
- `references/ANTENNA-RELAY-FSD.md` — full functional specification (v1.0.0)
- Transaction logging to `antenna.log` (metadata only; verbose mode optional)
- Sender validation against `allowed_inbound_peers` on receipt
- Outbound validation against `allowed_outbound_peers` on send
- `--dry-run` flag for envelope inspection without sending
- `--user` flag for optional humanized sender mode (experimental)
- Return-address headers for two-way messaging
- `main` session shorthand resolved to `agent:<local_agent_id>:main`

### Fixed (relative to v0.x development)
- `antenna-health.sh` updated from stale `.peers[]` registry format to current flat format
- `antenna-peers.sh` updated from stale `.peers[]` registry format to current flat format
- Removed stray `user_name` field from `antenna-config.json`
- Reconciled `relay_agent_model` across config and docs (now consistently `"openai/gpt-5.4"`)

### Architecture Decisions
- **Script-first**: all deterministic logic in bash scripts, not the LLM
- **Dedicated agent**: separate from primary assistant, minimal workspace/context (~2k tokens vs ~23k)
- **Plain relay default**: host-based envelope format is the stable path; humanized sender mode is opt-in
- **Fire-and-forget**: async messaging, no persistent connections, no blocking

### Known Limitations
- MCS (Malicious Content Scanning) designed but deferred — toggle exists in config, not yet implemented
- `--since` flag in `antenna log` not yet implemented (shows last N entries instead)
- Peer discovery is manual (no auto-discovery)
- Local model aliases may not resolve in all gateway agent configs — prefer a full provider/model ID in shareable skill defaults

## [0.x] — 2026-03-26 to 2026-03-28

Development iterations. Not individually versioned. See `references/ANTENNA-RELAY-FSD.md` revision history for details.
