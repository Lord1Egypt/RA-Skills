# Gemini CLI cross-agent verification — 2026-05-20

> **Verb naming note (added 2026-05-21)**: this report references `+publish` /
> `+unpublish` because that was the verb name in effect during the 2026-05-20
> run. On 2026-05-21 these verbs were **renamed to `+frequent` / `+unfrequent`**
> to better reflect their actual semantics ("设为常用" — pin to the caller's own
> workbench, **not** cross-user publishing). API endpoint + payload unchanged.
> The report below preserves the original terminology for historical accuracy.

**Status**: ✅ verified (with long-stream robustness gap surfaced + fixed)
**Skill**: cue-buddy v0.1.0
**Agent**: Gemini CLI
**Session window**: ~54 min (19:24 → 20:18 UTC+8)
**Trigger source**: user fetched `https://github.com/sensedeal/cue-skills/` as skill input

This report sediments what surfaced during the real-world Gemini CLI run so future contributors see how cross-agent verification drives skill hardening.

## Verbs exercised (in order)

| Verb | Outcome |
|---|---|
| Skill load (Gemini reads `cue-buddy/SKILL.md` via repo URL) | ✓ skill registered, +author trigger phrases recognized |
| `+list` (list user's templates) | ✓ returned existing template inventory |
| `+capabilities` | ✓ returned Cue researcher surface (~391 tools / ~56 categories / 10 presets, ETag-cached); user drilled into specific category for tool details |
| `+test <template_id> <entity>` on subject 第四范式 (A-share AI listed company `688310.SH`) | ⚠️ stream hit long-running deep research (>5min), client SSE disconnected before reporter agent started; script reported `no reporter content captured — check workflow_id / template_id`, **misleading user into thinking the template was broken** |

## What surfaced (real bug, not skill misuse)

User reasonably questioned the `check workflow_id / template_id` hint when the cuecue.cn web UI showed the report finished successfully on the same `conversation_id`. Diagnostic chain:

1. Server-side reporter agent completed and wrote report to DB ✓
2. Client SSE connection dropped around 372.9 seconds in (before reporter `start_of_agent` event reached the client)
3. `_extract_reporter_content(events)` returned empty string because no reporter window was ever entered
4. `+test` script exited 1 with hint pointing at template / workflow ID — wrong category of root cause

## Hardening that followed

Two codex review rounds (r4 + r5) drove these fixes — all merged to `main` and verified by CI:

### Round 4 (commit `720bf68`) — diagnose + replay fallback
- New `_diagnose_empty_report()` classifies empty-extraction into 4 kinds:
  - `stream_cut_before_reporter` (this Gemini case)
  - `reporter_started_no_text`
  - `no_agent_events`
  - `unknown`
- On `stream_cut_before_reporter`, the script now auto-calls `GET /api/replay/<conv_id>?resume=0` — pure DB replay, **no credit cost** — and re-extracts the report. The 8 acceptance checks then run as if the original stream had completed.
- Corrected an earlier mis-diagnosis (originally posited as "end_of_agent missing keeps the window open"): `in_reporter` defaults to `False` and only flips to `True` when `start_of_agent reporter` is seen, so a missing `end_of_agent` doesn't cause emptiness — the real root cause was `start_of_agent reporter` never reaching the client.

### Round 5 (commit `ad7bcb6`) — replay CLI + broader exception net
- `cue_api.py replay <conversation_id>` CLI subcommand added (with `--timeout` and `--report-only` flags), so the fallback hint message points at a real working command rather than `unknown cmd: replay`.
- `+test` chat_stream loop now catches `OSError, ValueError` in addition to `CueAPIError`, so transient `URLError` / `socket.timeout` / `ConnectionResetError` no longer skip the diagnose + replay path.

## Conclusion

- **Skill works on Gemini CLI** for the in-scope verbs (`+author`, `+list`, `+capabilities`, `+validate`, `+create`, `+update`, `+frequent` family — referenced as `+publish` in the original 2026-05-20 run; see verb naming note at the top).
- The single failure mode that surfaced (`+test` on long-running deep research) is now caught, diagnosed, and auto-recovered via replay without re-charging the user.
- This is the kind of failure that **only shows up in real cross-agent verification** — synthetic tests with short mock backends never trigger it. The Gemini CLI run paid for itself by uncovering it.

## Privacy / scrubbing

Source trace lives under `~/.gemini/tmp/<project>/chats/` (Gemini CLI's local chat history). It contains the user's API key in plain text on the first message that paste it in. Operators using this skill must:

- **Rotate the Cue API key** at `https://cuecue.cn/api-key` after any cross-agent session that involved pasting the key into chat (Gemini CLI / Codex / OpenClaw all persist chat history to disk by default).
- Treat `~/.gemini/tmp/` and equivalent dirs as containing secrets — never commit them, never share, never sync to public cloud.
- Use `export CUE_API_KEY=sk-...` in shell env or write to `~/.cue/config.json` (mode 600) so the key never enters chat content.

## References

- Commits: `720bf68` (diagnose + replay fallback), `ad7bcb6` (replay CLI + broader except)
- Skill regression tests covering this case: `cue-buddy/scripts/test_skill_regression.py:Case10_TestTemplateDiagnosis` (4 unittest)
- Skill mock-server contract: `cue-buddy/scripts/test_cue_api_client_contract.py` (10 unittest)

---

## v0.2.0 status update (2026-05-29)

> The run documented above was on **cue-buddy v0.1.0**. That header is left
> unchanged for historical accuracy — it records the version actually
> exercised on Gemini CLI on 2026-05-20. This section tracks where
> verification stands at the current **v0.2.0** manifest.

**What changed v0.1.0 → v0.2.0** (version bumped in commit `e472874`):

- `+publish` / `+unpublish` → **`+frequent` / `+unfrequent`** rename (the verb-naming note at the top of this report). API endpoint + payload unchanged.
- New **`+upgrade`** verb + session-start `--silent-check` (24h-cooldown GitHub-raw version compare; never prompts/auto-pulls).
- New sibling skill **`cue-research`** (use buddies / free-form deep research): Stage 2 single-stage full-list semantic picking, weak-match nudge, `/api/rewrite` free-form path.
- Quality rules codified for `title` and `goal` (R2 value-first card copy).
- Onboarding first-screen redesign + numbered `1/2/3` selection prompts.
- `tune_template` robustness: LLM-output parsing + format normalization + sub-section-safe renumber.
- Publishing-standards pass (2026-05-29): directory rename `buddy/` → **`cue-buddy/`** (matches `name:`), version reconcile across READMEs, trigger-focused description trims, and a declared cue-research → cue-buddy install dependency.

**v0.2.0 verification level** (what has actually been run):

| Layer | Status |
|---|---|
| Local stdlib regression — cue-buddy | ✅ 50/50 |
| Local stdlib regression — cue-research | ✅ 15/15 |
| `cue_api` mock-server contract | ✅ 14/14 |
| CI matrix (cue-buddy + cue-research × Python 3.12 / 3.13) | ✅ green (PRs #15, #16) |
| Adversarial codex review of the publishing-standards changeset | ✅ 4 PASS + 1 declined nit |
| **Live cross-agent run at v0.2.0 (driving the production API)** | ✅ **verified on Hermes, OpenClaw, Kimi** (real task run, live API) — among other agents |

**v0.2.0 live cross-agent verification:** beyond the local + CI coverage above,
v0.2.0 has been exercised with **real tasks against the production Cue API** on
**Hermes, OpenClaw, and Kimi** (among others). This closes the gap that the
v0.1.0 Gemini run alone left open: the new v0.2.0 surfaces — `+upgrade` and the
`cue-research` flow — now have live cross-agent coverage, not just local suites
+ CI. (The 2026-05-20 Gemini run above remains the detailed write-up because a
real bug surfaced there; these v0.2.0 runs are recorded here at summary level.)
