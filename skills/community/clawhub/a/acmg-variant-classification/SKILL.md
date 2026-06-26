---
name: acmg-variant-classification
description: Standard workflow for ACMG/AMP germline small-variant classification — collect evidence, assign criteria, detect conflicts, and produce a review-ready classification summary. Use when a user wants a structured ACMG/AMP-style interpretation workflow for a germline SNV/indel, including guided evidence intake, criteria assignment, conflict handling, and provisional classification.
---

# ACMG Variant Classification

Use this skill when a user wants a structured ACMG/AMP-style interpretation workflow for a germline SNV/indel.

## Interaction mode

Default to a guided interview workflow.

When using this skill with a live user:
1. Ask for one block of information at a time
2. Wait for the user's answer before moving on
3. Do not request all evidence at once unless the user asks for a bulk template
4. Explicitly track what is known, unknown, and still needed
5. Treat phenotype, family history, segregation data, and parental genotypes as user-supplied inputs that may arrive incrementally

Recommended guided sequence:
1. Variant identity: gene, transcript, build, c.HGVS, p.HGVS, variant type
2. Clinical phenotype / suspected disease
3. Inheritance model and family structure
4. Parental genotype status and de novo / segregation details
5. Population / database / literature evidence
6. Functional and computational evidence
7. Criteria assignment and final review

At each step, summarize back in one compact block:
- confirmed facts
- missing facts
- provisional ACMG implications

## Safety / scope

Always say clearly:
- This is decision support, not a final clinical diagnosis.
- Gene/disease-specific ClinGen guidance overrides generic ACMG rules where applicable.
- Final classification requires expert manual review.

## Inputs you should collect

Use templates/intake.md and ask for or normalize these fields:
- Gene
- Transcript
- Genome build
- c.HGVS
- p.HGVS
- Variant type
- Zygosity
- Inheritance model
- Phenotype / disease context
- Population frequency evidence
- Functional evidence
- Segregation / de novo evidence
- Database assertions
- Literature evidence

If transcript, genome build, or HGVS is unclear, stop and ask for clarification before classification.

## Standard workflow

### Step 1: Confirm scope
Proceed only if all are true:
1. Variant is a germline small variant (SNV/indel)
2. Naming/build/transcript are defined
3. User understands output is review-only
4. Any gene-specific ACMG framework has been checked

### Step 2: Normalize the record
Create a clean variant record using templates/intake.md.

### Step 3: Gather evidence by ACMG bucket
Pathogenic side:
- PVS1
- PS1, PS2, PS3, PS4
- PM1, PM2, PM3, PM4, PM5, PM6
- PP1, PP2, PP3, PP4

Benign side:
- BA1
- BS1, BS2, BS3, BS4
- BP1, BP2, BP3, BP4, BP5, BP7

### Step 4: Assign criteria carefully
Use templates/evidence-table.md.
For each criterion, record:
- code
- strength
- triggered yes/no
- reason
- source
- caveat / limitation

Do not double count overlapping evidence.

### Step 5: Evaluate conflicts
If both pathogenic and benign evidence exist:
1. Check whether evidence is truly independent
2. Downgrade/remove misapplied criteria if needed
3. If conflict remains unresolved, prefer VUS over forced certainty
4. State what additional data could resolve the conflict

### Step 6: Apply combination logic
Use scripts/classifier.py or reproduce its logic manually.

Pathogenic if any:
- 1 Very Strong + >=1 Strong
- 1 Very Strong + >=2 Moderate
- 1 Very Strong + 1 Moderate + 1 Supporting
- 1 Very Strong + >=2 Supporting
- >=2 Strong
- 1 Strong + >=3 Moderate
- 1 Strong + 2 Moderate + >=2 Supporting
- 1 Strong + 1 Moderate + >=4 Supporting
- >=3 Moderate + >=3 Supporting

Likely Pathogenic if any:
- 1 Very Strong + 1 Moderate
- 1 Strong + 1 to 2 Moderate
- 1 Strong + >=2 Supporting
- >=3 Moderate
- 2 Moderate + >=2 Supporting
- 1 Moderate + >=4 Supporting

Benign if any:
- BA1
- >=2 Strong benign criteria

Likely Benign if any:
- 1 Strong benign + 1 Supporting benign
- >=2 Supporting benign

Else: VUS

## Guided questioning pattern
Use short, sequential prompts:
- Step A: ask only for variant identity fields
- Step B: ask only for phenotype and suspected diagnosis
- Step C: ask only for pedigree / family history / inheritance
- Step D: ask only for parental genotypes and segregation/de novo details
- Step E: ask only for outside evidence such as ClinVar, literature, frequency, and functional assays
- Step F: summarize triggered or candidate ACMG criteria before giving a provisional class

## Included files
- templates/intake.md
- templates/evidence-table.md
- references/sop.md
- references/test_cases.json
- scripts/classifier.py
