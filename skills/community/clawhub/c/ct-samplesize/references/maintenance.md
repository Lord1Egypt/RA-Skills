# Maintenance Notes

> 从 SKILL.md 移出（2026-11-15）：回归测试 / Bug 上报 / 带日期变更说明等维护类内容，不应留在 SKILL.md，归档于此。

## Bug Reporting

Agent behavior only; implementation → `adapters/bug_report.py`, protocol → `references/bug_report_endpoint.md`.

- **Trigger (strong signal, max 1 proposal/session):** unexpected non-zero exit / engine or compute error / user explicitly questions the result — **and** the same operation was retried ≥1. Weak signal (repeated tuning) never triggers. Explicit user request (e.g., "report a bug") also triggers, without the once-per-session limit.
- **Two-stage confirmation:** ① propose-with-preview — show the bilingual `confirm_prompt` **with** the full sanitized report (`render_report_text`); user may add a `description` (re-render & re-show before consent) → ② on explicit consent, `send_to_endpoint` (action=report, endpoint `https://ct-bugreport.coze.site/run`). If declined, never re-propose this session.
- **Sanitization is hard:** report carries only the 11-key whitelist — never raw data or subject records. `description` is the only free-text field, **user-reviewed**; hard boundary: no identifiable person/institution/subject info. If the session had **no** cloud call, `save_local_report()` writes locally (data never leaves the machine).
- **Client-only:** send `report` only. Governance actions (get/update/download/delete) are reserved for `ct-update`; never call them here.


## permissions (original verbose block, archived 2026-11-15)

permissions:
  scope: "user-space-only"
  network: "required"
  network_note: "v5 requires the remote coze compute endpoint (CTSS_COZE_ENDPOINT, or CTSS_COZE_MOCK=1 for a local demo) — the published skill has no local compute fallback. Only trial-design parameters leave the machine (no patient data); every request also carries a hostname hash `query_origin` (sha256, for server attribution/rate-limit) and the OS-language-derived `locale`, and the skill version `skill_version` (read from the local SKILL.md, for per-version attribution of cloud usage). Outbound authorization gate: the public endpoint is pre-whitelisted in config/config.json auto_approve_endpoints (never prompts, but the assistant states what is sent on first use); user-custom endpoints trigger a one-time AUTH-BLOCK user confirmation before any data leaves the machine. Payloads are sanitized (PII stripped) before sending."
  filesystem: "writes figures to CTSS_OUTPUT_DIR (default ./outputs) and optional curve PNGs; otherwise read-only"
  data: "no patient/external data leaves the boundary — only trial-design parameters plus the hostname hash (query_origin), the skill version (skill_version) and locale metadata are sent to the coze service"
