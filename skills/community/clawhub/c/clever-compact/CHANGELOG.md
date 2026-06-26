## v2.2.5 — May 4, 2026
**Security documentation patch**
- Added `SECURITY.md` — full capability justification for ClawHub security review
- No functional changes; plugin behavior identical to v2.2.4
- Addresses false-positive ClawScan flag (issue openclaw/clawhub#1989)

---

## v2.3.0 — April 15, 2026
**OpenClaw 2026.4.10+ compatibility fix — required update**

If you updated OpenClaw to 2026.4.10 or later and your agent stopped restoring memory between sessions, this is the fix.

*What broke:* CC v2.2.x relied on manual config references to load the plugin. OpenClaw 2026.4.10+ tightened plugin loading — only plugins properly installed via `openclaw plugins install` are activated. Manually referenced plugins were silently ignored with no error message.

*What's fixed:*
- Plugin must now be installed via `openclaw plugins install` (not manual config edits)
- Compiled `index.js` added alongside `index.ts` for environments where TS transpilation is restricted
- Ownership fix documented for Linux/VPS installs (uid mismatch from Mac-origin files)
- All functionality identical to v2.2.3 — state files, injection, `clever-compact:write` fn all unchanged

*To upgrade — 3 commands:*
```
openclaw plugins install clawhub:clever-compact
openclaw plugins enable clever-compact
openclaw gateway restart
```

*Linux/VPS only — if you see "suspicious ownership" warning:*
```
chown -R root:root ~/.openclaw/extensions/clever-compact
openclaw gateway restart
```

*Bonus: unrelated crash fix*
If sessions are also going dark due to a broken `codex` provider in `models.json` (leftover from earlier OC experiments), check and reset:
```
cat ~/.openclaw/agents/main/agent/models.json
# If you see a "codex" block with chatgpt.com/backend-api, reset it:
echo '{"providers":{}}' > ~/.openclaw/agents/main/agent/models.json
openclaw gateway restart
```

Tested on OC 2026.4.14. No breaking changes to state file format — existing `compact-state-*.md` files carry over automatically.

---

## v2.2.3 — March 16, 2026
**Version sync + docs accuracy patch**
- All version references now consistent across package.json, openclaw.plugin.json, index.ts, and SKILL.md (were mismatched across 2.1.0/2.2.0/2.2.2)
- Fixed install step count in description: "3 commands" → "4 steps" (install, allowlist, restart gateway, flush trigger)
- Updated recommended OpenClaw version: 2026.3.12+ (fixes double-compaction loop that could interfere with flush timing)
- Rewrote "why explicit write is fine" section — removed defensive framing, stated the architecture plainly
- No functional changes to the plugin

## v2.2.0 — March 11, 2026
**Per-turn injection fix**
- Fixed: state file was being prepended to every prompt turn (mid-session token overhead). Now injects ONCE at session start only.
- Added `clever-compact:write` fn exposure for programmatic state writes from heartbeats, cron, and other tools.
- SKILL.md updated to accurately document the write side as explicit/triggered, not automatic.
- No breaking changes; existing state files and cron setup carry over.

## v2.1.0 — March 8, 2026
**Architecture fix — lifecycle hooks only, no context engine registration**

v2.0.0 was yanked. The `registerContextEngine` approach had a critical bug: `compact()` returning `{ compacted: false }` blocked the legacy compaction engine instead of passing through to it. Any user who installed v2.0.0 and set the `contextEngine` slot would have had compaction silently stop firing.

v2.1 removes `registerContextEngine` entirely. The plugin registers one lifecycle hook:

- `before_prompt_build` → injects the most recent state file ONCE per session start (bootstrap/restore). Fires on first turn only — no per-turn token overhead.

**Note on write side:** OpenClaw does not expose a pre-compaction lifecycle hook. State writes are always explicit — triggered by your agent (manual phrase, heartbeat step, or pre-compact cron). The plugin exposes `api.fn("clever-compact:write")` for programmatic triggers. See SKILL.md for setup patterns.

Zero interference with the compaction mechanism. Installation no longer requires setting `plugins.slots.contextEngine` — just add `clever-compact` to `plugins.allow`.

## v2.0.0 — March 8, 2026 ⚠️ YANKED
Do not install. `registerContextEngine` + `compact()` returning `{ compacted: false }` caused compaction to silently stop firing for any user with the contextEngine slot set.

# Clever Compact — Changelog

## v1.2.0 — March 4, 2026
**Framing update — now speaks the language of the problem**
- Reframed the opening around the three failure modes: `/new` amnesia, compaction loss, memory drift
- Language mirrors how power users actually describe the problem — makes it immediately recognizable
- No functional changes to the skill itself

## v1.1.0 — March 3, 2026
**Reduce compaction frequency**
- Added `reserveTokens` tuning guide — lower from 50,000 to 15,000 to push compaction to ~185k/200k context
- Roughly 3–4× fewer compactions per heavy session
- Updated urgency language: compaction takes up to 10 minutes, not seconds. Real discovery from live power-user sessions.

## v1.0.0 — March 1, 2026
**Initial release**
- Core pre-compact scan: active workstreams, key decisions, open tasks, relationship context, remember flags
- State file written to `memory/compact-state-YYYY-MM-DD-HH.md`
- Post-compact restore hook via AGENTS.md
- State file format spec (Markdown + embedded JSON)
- Pro tier placeholder ($9/mo — feature-gated)
