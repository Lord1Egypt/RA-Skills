# Bug Report Endpoint Protocol (ct-samplesize)

> Detailed protocol for `adapters/bug_report.py`. The SKILL.md `## Bug Reporting` section keeps only the agent-facing behavior rules; implementation specifics live here.

## Trigger

Two paths:

- **(A) Explicit user request** — "report a bug" / "反馈问题" / "提交错误报告": go straight to two-stage confirmation, no strong signal needed, **unlimited per session**.
- **(B) Strong signal** — CLI non-zero exit / engine error / user questions correctness — **and** the same operation was retried ≥1 → **at most 1 unsolicited proposal per session**.
- Weak signal (just repeated tuning) never triggers.
- Explicit user request takes priority over the once-per-session cap.

## Two-stage confirmation (2026-08-21, simplified from three-stage)

1. **Propose-with-preview** — give the bilingual `confirm_prompt` **together with** the full report (`render_report_text`). State "sanitized, no input data" and invite a problem description. If the user adds a `description`, re-render and re-show before consent.
2. **On explicit consent** → `send_to_endpoint` (auto `action=report`, endpoint `https://ct-bugreport.coze.site/run`, `token` = embedded public credential).
3. If the user declines, **never re-propose this session**.

## Sanitization (hard rule)

- Report contains **only** the 11-key whitelist: `skill` / `version` / `test` / `error_type` / `error_code` / `engine_status` / `description` / `locale` / `query_origin` / `session_hash` / `attempts` — never raw data files or subject records.
- `description` is the single free-text field for debugging, **user-reviewed disclosure**: write symptom / reproduction / expected vs actual / **algorithm or function used** (e.g. Schoenfeld formula) / error message. Values and study design (HR, power, allocation ratio) are OK if needed to reproduce.
- **Hard boundary**: no identifiable person / institution / subject info.
- The user reviews `description` in the stage-① preview before consent. Empty `description` omits the key (old-endpoint compatible).
- If the session had **no** coze call, use `save_local_report()` (local md + author email, data never leaves the machine).

## Post-send history receipt (2026-08-22)

After a successful send, the endpoint returns `history` (last submission for the same `query_origin`, or `""`). Compose the reply from `confirm_thanks(locale)` + `build_followup(history, locale)` — bilingual, auto-switched by `locale`:

- empty `history` → end;
- `history.resultstr == "done"` → also show the fix note from `history.memo`;
- otherwise show "not yet fixed".

All user-facing strings are bilingual via `_MSGS` and `_current_locale()` auto-detection.

## Client-only boundary

This adapter sends `report` only. The governance actions (get / update / download / delete — pull pending, mark done, download all, clean up) are reserved for the `ct-update` skill (author side); **never call them from here**.
