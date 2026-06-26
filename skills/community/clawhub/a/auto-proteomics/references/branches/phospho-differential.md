# Phospho Differential Branch Spec

- route id: `phospho-differential`
- status: `scaffold`
- scientific goal: perform phosphosite-level downstream differential analysis from processed phosphoproteomics quantification results

## Expected upstream input family

This branch is for processed phosphosite-level quantification outputs, not raw phosphoproteomics search pipelines.

## Required files

- phosphosite quantification table
- sample annotation table

## Optional files

- protein mapping table
- localization confidence table
- parameter export

## Minimal execution command pattern

```bash
bash scripts/workflows/phospho_differential.sh \
  --input-table <phospho_sites.tsv> \
  --sample-sheet <samples.tsv> \
  --output-dir <output_dir> \
  --group-a <condition_a> \
  --group-b <condition_b>
```

## Expected outputs

- site-level filtered matrix
- phosphosite QC summary
- differential phosphosite table
- run manifest
- report

## Out-of-scope

- raw phosphoproteomics search and identification
- PTM localization rescue from incomplete upstream data
- pathway enrichment as an implied default step
- multi-factor statistical designs in the first release

## Validation target

At minimum, this branch should validate:
- phosphosite identifier structure
- sample mapping
- site-level missingness handling
- group comparison integrity
- stable report generation

## Release-readiness checklist

- route wording is unambiguous
- phosphosite-specific input contract is explicit
- one clear execution file exists
- one small-model-readable command pattern exists
- outputs are explicit
- out-of-scope behavior is explicit
