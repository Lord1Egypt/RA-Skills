# ACMG Variant Classification SOP

Purpose: provide a repeatable ACMG/AMP-based workflow for germline SNV/indel interpretation.

## Scope
Use for:
- germline SNV / indel
- review-oriented variant interpretation
- standardized evidence capture

Do not use as-is for:
- CNV / SV
- somatic oncology
- mitochondrial variants
- final unsupervised clinical reporting

## Core process

### 0. Precheck
Confirm:
- sample and variant identifiers are unique
- transcript is fixed
- genome build is fixed
- HGVS naming is coherent
- gene/disease-specific ACMG guidance was checked

### 1. Intake
Collect variant identity, phenotype context, inheritance model, source list, and missing data.

### 2. Evidence gathering
Review all ACMG evidence buckets, not only the obvious ones.

### 3. Criteria assignment
For each criterion record:
- yes/no
- justification
- source
- caveat

### 4. Anti-double-counting review
Do not stack overlapping evidence from the same underlying dataset.

### 5. Conflict review
If pathogenic and benign evidence coexist, prefer explicit conflict analysis over forced upgrading.
Unresolved conflict should usually remain VUS.

### 6. Combination logic
Use ACMG/AMP combination rules, ideally after manual confirmation of all triggered criteria.

### 7. Independent review
Check especially:
- transcript correctness
- LoF mechanism before PVS1
- frequency thresholds for BA1/BS1/PM2
- improper PP3/BP4 inflation
- unsupported ClinVar overreliance

### 8. Archive
Store:
- normalized variant description
- evidence table
- final logic summary
- reviewer/date/version
- reclassification triggers

## Minimum reportable output
- Normalized variant descriptor
- Triggered evidence codes
- Conflict explanation
- Final provisional ACMG class
- Review limitations
- Reclassification triggers
