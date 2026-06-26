---
name: auto-proteomics
description: Public OpenClaw skill for low-token routing and downstream analysis of processed DDA LFQ proteomics inputs. Use when the user already has protein-level quantification tables such as MaxQuant-style `proteinGroups.txt` and needs a clear two-group downstream workflow.
---

# Auto Proteomics

Author: Guo Xuan 郭轩  
Contact: xguo608@connect.hkust-gz.edu.cn

`auto-proteomics` is a public `v0.x` skill for processed proteomics downstream work.

The current public promise is intentionally narrow:
- one shipped runnable workflow: `dda-lfq-processed`
- one public input family: processed DDA LFQ protein-level tables
- one public comparison model: `group-a` vs `group-b`

Everything else in this repository should be read as routing context, internal prototype, or future scaffold unless a document explicitly marks it as part of the public promise.
Presence of a script, schema, or branch document does not mean the route is publicly supported.
In particular, `dia-quant` is intentionally exposed as an internal prototype route for correct routing and contract validation, not as a shipped public workflow.

## Use this skill when

- the user already has processed protein-level quantification output
- the main table is MaxQuant-like `proteinGroups.txt`
- the goal is QC, normalized matrix generation, and two-group differential protein analysis
- the user wants a low-token, file-driven workflow instead of a long chat-only protocol

## Do not use this skill when

- the user starts from raw spectra and needs search/identification
- the request is primarily DIA, phosphoproteomics, enrichment, or multi-omics execution
- the task requires more than one comparison design in the current release
- the user only wants generic statistics with no proteomics context

## Public promise in `v0.x`

Shipped and supported now:
- route processed DDA LFQ downstream requests into `dda-lfq-processed`
- validate the expected processed-input shape
- generate matrix, QC, differential tables, report, and manifest outputs

Not promised yet:
- raw-spectrum search pipelines
- DIA public execution support
- phosphoproteomics execution
- enrichment execution
- multi-omics execution
- generalized study-design handling beyond the current two-group path

Internal prototype route available for routing only:
- `dia-quant` may be selected only when the request is explicitly about processed DIA quant tables that fit the checked-in DIA contract
- selecting `dia-quant` means internal prototype triage, never a public `v0.x` execution recommendation

Important boundary:
- non-shipped branches may contain scaffold or prototype execution files for internal framework development
- smaller models must not treat those files as public runnable recommendations unless a route is explicitly marked `shipped`

## Minimal workflow

1. Read `references/WORKFLOW_INDEX.yaml`
2. If the route is unclear, run `scripts/decision/route_proteomics.py`
3. Check that the request fits the public `v0.x` boundary
4. Run `scripts/workflows/dda_lfq_processed.sh`
5. Use `references/` for runtime, onboarding, and development rules

## Public runnable entrypoint

```bash
bash scripts/workflows/dda_lfq_processed.sh \
  --input-dir <run_dir> \
  --protein-groups <proteinGroups.txt> \
  --summary <summary.txt> \
  --parameters <parameters.txt> \
  --output-dir <output_dir> \
  --group-a <condition_a> \
  --group-b <condition_b>
```

## Input contract

Required:
- `proteinGroups.txt` with `LFQ intensity *` or `Intensity *` columns
- `summary.txt` with `Raw file` and `Experiment` columns

Optional:
- `parameters.txt`

## Output contract

The shipped workflow produces:
- normalized protein matrix files under `matrix/`
- QC outputs under `qc/`
- differential protein tables under `stats/`
- `REPORT.md`
- `summary.json`
- `run_manifest.json`

## Repository layers

- `SKILL.md`: public entry and release boundary
- `references/WORKFLOW_INDEX.yaml`: machine-readable routing and shipped-vs-non-shipped map
- `references/BRANCH_FRAMEWORK.md`: standard branch contract for future routes
- `references/branches/`: per-branch specs for scaffold and prototype workflows
- `references/DIA_INPUT_SCHEMA.md`: first narrow schema for DIA prototype intake
- `scripts/workflows/dda_lfq_processed.sh`: shipped workflow entrypoint
- shipped public guidance lives in documents that explicitly describe the processed DDA `v0.x` path
- non-shipped reference docs exist for internal framework development and must not be surfaced as public support

## Read next

- `references/WORKFLOW_INDEX.yaml`
- `references/RUNTIME_REQUIREMENTS.md`
- `references/BRANCH_FRAMEWORK.md`
- `references/DEMO_INPUT_GUIDE.md`
- `references/DEVELOPMENT_GUIDE.md`
