# Maintenance Notes

> 从 SKILL.md 移出（2026-11-15）：回归测试 / Bug 上报 / 带日期变更说明等维护类内容，不应留在 SKILL.md，归档于此。

## Regression Tests

Maintainer-only (stdlib, no pytest; **not shipped**): `python tests/mode_b_test.py` (10 hardening cases) and `python tests/mode_c_test.py` (F1–F11). Both offline by default. Details in `references/errors.md`.

## Bug Reporting (ct-base §20.3, adapter: `adapters/bug_report.py`)
Propose **at most once per session**, only on a strong signal **and** after ≥1 retry — never on repeated tuning. Always two-stage: ① show the sanitized report → ② send only on explicit consent; never re-propose after a decline. Full rules, 11-key whitelist, and CLI: `references/bug_reporting.md`.

**2026-10-26 · ct-base §22.27 ML data-quality monitoring**: ML data-quality monitoring sits as a supplementary layer (CM1–CM2) on top of conventional QC (CM0), targeting detection of centre effects, data drift, and systematic entry errors in psychotropic-drug / chronic-disease RCTs; three elements must be pre-specified — an upper bound on the false-positive rate, alert thresholds, and an escalation path (NCI/Zenodo 2026-10-18).


## permissions (original verbose block, archived 2026-11-15)

permissions:
  scope: "user-space-only"
  network: "public-retrieval"
  network_note: "Reads only public sources: FDA FAERS / openFDA (https://api.fda.gov/drug/event.json), optional China PV (cdr-adr.org.cn, no WAF/no key), and optional corroborative sources via corroborative_sources.py — dailymed.nlm.nih.gov (SPL labels), rxnav.nlm.nih.gov (RxClass MED-RT), api.fda.gov drug/enforcement (recalls); all keyless public. No confidential input; ordinary input + public retrieval (A-tier, network=public-retrieval per ct-base §11). NMPA main site is WAF-blocked (HTTP 412) and intentionally excluded. Count-source feasibility is verified per-source (multi_source.COUNT_SOURCE_FEASIBILITY): PMDA JADER (captcha), Health Canada (timeout), VAERS (403), EudraVigilance (BO report, no JSON), VigiAccess (SPA, no API), MHRA iDAP (timeout) are verified blocked/unreachable on 2026-09-01 and intentionally excluded — not silently dropped. Low-frequency, keyless FAERS; optional --api-key raises quota. All retrieval (faers / fda_label / dailymed / rxclass / fda_recall / hk_pv / nmpa_pv) is OUTBOUND to the ct-registry unified endpoint ct-search.coze.site (thin local client). No local fallback path since v0.9.9."
  filesystem: "read-only to its own files; writes outputs ONLY to the user-specified --out-dir (default: current working directory). No system-path or hidden logging; any operational log (e.g. safety_err.log) is written under --out-dir (out_live/), never outside it, and FAERS raw responses are not persisted unless the user explicitly saves them."
  data: "no confidential data input. Retrieval requests (drug/event public query keywords) are sent to the ct-registry unified endpoint ct-search.coze.site (thin local client). Only public query parameters + public retrieval results cross the boundary; no confidential user data is ever transmitted."

## Dev artifacts excluded from every publish target (moved from SKILL.md)

The `tests/` directory (regression harness) is not tracked by git and is shipped to **no** publish target — GitHub, ClawHub, or SkillHub (ct-base §16.8). It stays on the maintainer's local disk only; the installed package contains no test code.
