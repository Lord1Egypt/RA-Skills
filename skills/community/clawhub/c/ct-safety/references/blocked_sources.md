# ct-safety — Blocked / Excluded Safety Sources (verified 2026-09-01)

Not silently dropped — each was tested from this machine; reasons are also recorded in
`multi_source.COUNT_SOURCE_FEASIBILITY` / `corroborative_sources.BLOCKED_SOURCES`.

| Source | Status |
|---|---|
| PMDA JADER (Japan) | Not automatable (live) — captcha; full DB CSV obtainable (planned) |
| Health Canada (live API) | Legacy API unreachable; open-data ZIP planned |
| VAERS / CDC WONDER | Needs data-use agreement (403) |
| EudraVigilance (EMA) | Needs authorization |
| VigiAccess / VigiBase (WHO) | No public API (SPA; full access paid) |
| MHRA iDAP (UK) · Taiwan FDA PV | Unreachable locally |

Re-test before claiming "no data" — conditions may change.

## Planned (deferred 2026-09-01)

T1 trio — Health Canada bulk ZIP / PMDA JADER full CSV / TGA DAEN live retrieval.
Feasibility, access models, and architecture → `references/roadmap_external_sources.md`.
