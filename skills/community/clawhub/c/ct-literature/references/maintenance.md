# Maintenance Notes

> 从 SKILL.md 移出（2026-11-15）：回归测试 / Bug 上报 / 带日期变更说明等维护类内容，不应留在 SKILL.md，归档于此。

## Bug Reporting (§20.3, adapter: `adapters/bug_report.py`)

Trigger = explicit user request (unlimited) or strong signal + one retry (≤1 proposal/session). Hard two-stage confirmation: ① show full sanitized report → ② send only on explicit consent (endpoint `https://ct-bugreport.coze.site/run`, public credential). 11-key whitelist envelope,
`description` is the only user-reviewed free text; never raw data. Client sends `report` only —
governance belongs to `ct-update`. Full trigger/two-stage/sanitization detail → [references/dialogue.md](references/dialogue.md).


## permissions (original verbose block, archived 2026-11-15)

permissions:
  scope: "user-space-only"
  network: "optional"
  network_note: "Reads only public bibliographic sources: OpenAlex (api.openalex.org, no key), Europe PMC (ebi.ac.uk, MEDLINE/MeSH, no key; also indexes bioRxiv/medRxiv preprints via SRC:PPR), Semantic Scholar (api.semanticscholar.org, no key; rate-limited HTTP 429 -> gracefully skipped), arXiv (export.arxiv.org/api/query, no key). Europe PMC is ON by default (--no-with-europepmc to disable); bioRxiv/medRxiv are ON by default (--no-with-biorxiv / --no-with-medrxiv to disable); arXiv is opt-in via --with-arxiv. No WAF, no confidential input; ordinary input + public retrieval (A-tier). Opt-in, user-confirmed bug reports additionally reach https://ct-bugreport.coze.site/run with an 11-key sanitized envelope only (never raw data)."
  filesystem: "read-only to its own files; writes report files only to the current working directory"
  data: "no confidential data input; no external transmission of user data"
