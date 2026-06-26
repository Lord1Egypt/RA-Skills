# Release Checklist

Use this checklist before the next public Auto-Proteomics release.
The goal is not to make the repository look smaller than it is.
The goal is to keep the public claim honest while excluding packaging residue and demo-only outputs.

## Release boundary for the next public version

Publicly shipped now:
- `dda-lfq-processed`
- processed DDA LFQ protein-level downstream analysis
- one clear two-group comparison path: `group-a` vs `group-b`

Not publicly shipped yet:
- `dia-quant`
- `dda-identification`
- `phospho-differential`
- enrichment execution
- multi-omics execution

Prototype or scaffold files may remain in the repository if their status stays explicit.
They must not be described as shipped support.

## Required release checks

1. Rebuild a clean staged tree instead of packaging the live repository directly.

```bash
python3 scripts/release/stage_release.py
```

2. Inspect the staged public surface only:
- `SKILL.md`
- `README.md`
- `RELEASE_SUMMARY.md`
- `references/WORKFLOW_INDEX.yaml`
- `references/branches/dia-quant.md`
- `examples/demo_processed_dda/README.md`
- `examples/demo_dia_proto/README.md`

3. Confirm public wording is still honest:
- only `dda-lfq-processed` is marked `shipped`
- DIA remains `prototype` and `not shipped`
- no doc says DIA is public, supported, validated, or release-ready
- no doc implies raw DDA, phospho, enrichment, or multi-omics execution are shipped

4. Confirm package hygiene:
- no `dist/` content inside the packaged skill
- no `.git/` content inside the packaged skill
- no `__pycache__/` or `*.pyc`
- no `examples/*/results/`
- no `NEXT_STEPS.md` or `ROADMAP.md`
- no `mock` or other fake-validation residue

5. Rebuild the package and run the archive check:

```bash
python3 scripts/release/build_skill_package.py
python3 scripts/release/check_public_package.py
```

6. Spot-check routing behavior before release:

```bash
python3 scripts/decision/route_proteomics.py \
  --data-type proteomics \
  --acquisition-mode dda \
  --input-stage processed-table \
  --target-output differential-analysis \
  --pretty

python3 scripts/decision/route_proteomics.py \
  --data-type proteomics \
  --acquisition-mode dia \
  --input-stage processed-table \
  --target-output quantification \
  --pretty
```

Expected:
- DDA processed downstream returns `public-match`
- DIA returns out-of-scope for public `v0.x`

## Release decision rule

Do not publish if any of these are true:
- a non-shipped route is described as public support
- staged or packaged contents include demo results or development residue
- the router recommends anything other than `dda-lfq-processed` as public support
- the release notes claim broader proteomics coverage than the checked-in public boundary

## Notes for future expansion

When a new route becomes truly public, update all of these together:
- `SKILL.md`
- `README.md`
- `references/WORKFLOW_INDEX.yaml`
- the branch spec under `references/branches/`
- this checklist
