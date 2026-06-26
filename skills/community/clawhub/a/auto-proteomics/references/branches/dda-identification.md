# DDA Identification Branch Spec

- route id: `dda-identification`
- status: `scaffold`
- scientific goal: take processed or exported DDA identification results and prepare a stable identification-to-downstream handoff path

## Expected upstream input family

This branch targets DDA identification-stage exports from software such as MaxQuant, FragPipe, or MSFragger-related result tables.

## Required files

- protein-level identification or quantification table
- peptide evidence or equivalent mapping table
- sample annotation or run summary table

## Optional files

- parameters export
- search settings export

## Minimal execution command pattern

```bash
bash scripts/workflows/dda_identification.sh \
  --input-dir <run_dir> \
  --output-dir <output_dir>
```

## Expected outputs

- validated identification summary
- standardized protein-level handoff files
- run manifest
- report

## Out-of-scope

- vendor raw file processing in the first release
- universal support for every search engine without explicit adapter rules
- full downstream biological interpretation as part of identification itself

## Validation target

At minimum, this branch should validate:
- presence of expected exported tables
- required identifier columns
- handoff readiness into downstream protein-level workflows

## Release-readiness checklist

- route wording is unambiguous
- supported upstream families are explicit
- handoff contract to downstream analysis is explicit
- one clear execution file exists
- out-of-scope behavior is explicit
