---
name: egfr-batch
description: Batch-compute eGFR with the published CKD-EPI 2021 equations from a CSV of age, sex and creatinine, with the creatinine unit (mg/dL or umol/L) declared explicitly — the tool refuses to guess it. Optionally adds cystatin-C eGFR, Cockcroft-Gault and de-indexed values. Use when asked to calculate eGFR for a cohort or CSV file, run one CKD-EPI calculation, or convert creatinine units for eGFR. Not for general lab-unit conversion (use labunits), child growth z-scores (use growthz), de-identification checks (use safeharbor-check), or randomisation lists (use blockrandom). Research/educational only; not a medical device.
license: MIT
compatibility: Requires Python 3.10+, standard library only, no dependencies. Installing needs network access to GitHub; the tool itself runs fully offline and files never leave the machine.
---

# egfr-batch

## What this tool does

egfr-batch computes eGFR for a CSV of people with the published CKD-EPI
2021 equations (creatinine, and creatinine–cystatin C where cystatin C is
given), returning the same CSV with the results, the converted creatinine
actually used, and a per-row column naming the exact equation behind each
number. It refuses to run unless the creatinine unit is declared: mg/dL
and µmol/L differ by a factor of 88.4, and a guessed unit silently
corrupts every row. It does arithmetic only — no diagnosis, no staging,
no interpretation.

## Install

```bash
pip install git+https://github.com/RakTikoo/egfr-batch
```

This provides the `egfr-batch` command. Verify an install with
`egfr-batch check` (recomputes a published worked example; prints PASS).

## Run

```bash
egfr-batch convert patients.csv --scr-unit mg/dL --scys-unit mg/L --cockcroft-gault --cg-weight actual --deindex --out patients_egfr.csv
egfr-batch single --age 60 --sex F --scr 106 --scr-unit umol/L --scys 1.2 --scys-unit mg/L
```

- Input columns are `age`, `sex` (`F`/`M`), `creatinine`, plus optional
  `cystatin_c`, `height_cm`, `weight_kg`.
- `--scr-unit` is required: `mg/dL` or `umol/L`. µmol/L values are
  converted with the NIDDK factor (÷ 88.4); the value used is written to every row as `scr_used_mg_dl`.
- If any row has cystatin C, `--scys-unit mg/L` is required.
- `--cockcroft-gault` requires an explicit `--cg-weight` of `actual`,
  `ideal` or `adjusted`; the weight used is recorded per row.
- `--deindex` adds eGFR in mL/min using Mosteller BSA; it needs
  `height_cm` and `weight_kg` on every row.

## Reading the results

Exit code `0` means the run computed. The summary states the declared
unit, which equations ran on how many rows, the Cockcroft-Gault weight
choice, and the output file. Output values are rounded to 1 decimal
place (`scr_used_mg_dl` keeps 4, so the conversion is auditable), and
each result column is paired with a provenance column naming its
equation and version.

Exit code `2` means the tool refused and **no output file was written**:
a missing `--scr-unit`, cystatin C without `--scys-unit`, an age under
18 or over 130, a missing, non-numeric or non-positive value, or
Cockcroft-Gault without a declared weight choice. One bad row refuses
the whole run, with the row number in the error — there is no partial
output to misread.

## Limits

- **Research and educational tool only. Not a medical device.** This
  tool does published-formula arithmetic only — it does not diagnose,
  stage, or interpret anything. Verify any result before clinical use.
- Arithmetic only, by design: no CKD staging, no diagnosis, no
  reference-range flagging, no interpretation. What a number means for a person is a clinical judgement this software does not make.
- Adults only: ages under 18 are refused. The CKD-EPI 2021 equations are
  adult equations; there is no paediatric equation in this tool.
- Assay assumptions are yours: the equations assume standardised
  (IDMS-traceable) creatinine and reference-standardised cystatin C; the tool cannot tell whether laboratory values meet that.
- eGFR is an estimate, not a measurement; known non-GFR determinants of
  creatinine and cystatin C (muscle mass, diet, some medicines, illness)
  affect the inputs and therefore the outputs.
- The published equations define female/male coefficients only; sex
  values outside `F`/`M` are refused rather than mapped to something the
  publication does not define.
