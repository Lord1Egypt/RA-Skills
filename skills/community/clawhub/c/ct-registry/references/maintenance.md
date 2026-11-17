# Maintenance Notes

> 从 SKILL.md 移出（2026-11-15）：回归测试 / Bug 上报 / 带日期变更说明等维护类内容，不应留在 SKILL.md，归档于此。

## Bug Reporting (ct-base §20.3, adapter: `adapters/bug_report.py`)

Trigger (explicit request → two-stage confirmation; strong signal + retry ≥1 → ≤1 unsolicited proposal/session), two-stage confirmation, post-send history receipt, 11-key sanitization whitelist, client-only scope → **`docs/bug_reporting.md`**. Invoke: `python adapters/bug_report.py --error-type <t> --description "<free text>" [--send]` (add `--send` only after the user confirms).

**2026-10-26 · ct-base §22.24 dual-track governance framework**: this skill touches both tracks of the dual classification — AI-as-intervention (AI as the evaluated intervention) and AI-for-trial-operations (AI as operational support); AI-as-intervention requires prospective registration + SPIRIT-AI/CONSORT-AI, whereas AI-for-trial-operations requires workflow-accuracy validation + TRIPOD-AI/ICH E6(R3) (EClinicalMedicine 2026-10). Continuously-learning systems require version locking + drift monitoring + rollback as a three-part package.


## permissions (original verbose block, archived 2026-11-15)

permissions:
  scope: "user-space-only"
  network: "optional"
  network_note: "Auto-direct public-retrieval sources: ClinicalTrials.gov v2 + PubChem (public REST API, ordinary input + public retrieval, B-tier). EU CTIS supports retrieve-by-number only (no search). China CDE blocks automated browsers via WAF -> external workflow for automatable retrieval (third-party endpoint, public query terms + non-content request metadata egress - query_origin machine-hash, skill_version, entry_point, params.user_language, demand_id; endpoint credential bundled in-package (shared public token, no user-side configuration — verified: HTTP 401 without it, i.e. the token ships with the skill); search/detail FIXED & verified 2026-07-23, all four modes end-to-end). ChiCTR / ISRCTN / DRKS are ALSO served by the same unified endpoint (source=chictr|isrctn|drks, third-party, shared Bearer) - so their query terms egress with the same metadata too. The bundled Bearer is a long-lived SHARED public credential issued by the author (XOR+base64 obfuscated, recoverable from the package); treat it as the endpoint's key, NOT your personal secret, and rotate/stop using if abused. CDE also supports an optional commercial API key (--cde-api-key) sent to the DXY commercial CDE-mirror API (api.dxy.cn), opt-in. All paths require zero confidential data or information input; only public query terms and the non-content metadata above ever leave the environment."
  filesystem: "read-only to its own files; writes report/Excel files to current working directory; download_docs.py can optionally write retrieved EU-CTR PDFs to a user-specified --out-dir"
  data: "no confidential data input; public query terms plus non-content request metadata (query_origin machine-hash, skill_version, entry_point, user_language, demand_id) are transmitted via the unified endpoint / optional DXY CDE-mirror API; no user files or secrets are sent"
