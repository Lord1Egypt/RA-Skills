# ct-registry — Publishing (ct-base §16)

Shared assets (`i18n.py`, `kw_localize.py`, `keyword_breadth.py`, `excel_style.py`,
`drug_name_resolver.py`, `source_guard.py`, `r_libs.py`, `office_to_md.py`, `merge_spec.py`,
and the JSON lexicons/maps) are **single-source in `ct-base`** (§16.8). `ct-registry` only
vendors synced copies; never edit a shared file locally and ship it — publish will silently
overwrite local edits with the `ct-base` version, losing your change. Fix in `ct-base` first,
then sync down.

**Mandatory pre-publish gate (run from the dev workspace where `ct-base` is a sibling):**

```bash
python scripts/publish_preflight.py            # resolves ct-base as ../ct-base
# or explicit:
python scripts/publish_preflight.py --base-dir ../ct-base
```

`publish_preflight.py` runs, in order:
1. `shared_sync_check.py` — blocks (exit 1) on any JSON or **Python** shared-module drift
   vs `ct-base` (§16.8 invariant; Python modules added 2026-08-27 — previously only JSON was
   checked, so `.py` forks went undetected).
2. `publish_secret_scan.py` — blocks on committed secrets / tokens.
3. `clawhub_security_audit.py --warn-only` — informational ClawHub term-audit (network; never blocks).
4. `publish_inject.py --dry-run` — previews which `ct-base` assets would be injected.

Only when `publish_preflight.py` exits 0 may you proceed:

```bash
python ../ct-base/scripts/publish_inject.py .          # inject shared assets (makes package self-contained)
# ... package & publish to GitHub → SkillHub → ClawHub (ClawHub: no --version) ...
python ../ct-base/scripts/publish_inject.py . --clean  # remove injected copies (auto-generated artifacts)
```

The `scripts/publish_preflight.py` orchestrator is **dev-only** (references the `ct-base`
sibling) and is excluded from the published package via `.clawhubignore`.
