## Description:

Computes CKD-EPI 2021 eGFR values from CSV or single-person inputs with explicitly declared creatinine units and optional cystatin C, Cockcroft-Gault, and de-indexing calculations.

This skill is for research and development only.

## Publisher:

[raktikoo](https://clawhub.ai/user/raktikoo)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers and developers can calculate adult eGFR values for a CSV cohort or a single input, using declared creatinine units and optional cystatin C, Cockcroft-Gault, or de-indexed calculations. The tool is for research and education and does not diagnose, stage, or interpret results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing from a Git URL requires trusting the linked package source.

Mitigation: Review the package source before installing.

Risk: Research or educational eGFR calculations could be mistaken for clinical diagnosis or interpretation.

Mitigation: Use for research and education only; do not use the results to diagnose, stage, or interpret a person's condition.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/raktikoo/skills/egfr-batch)
- [Package source and installation instructions](https://github.com/RakTikoo/egfr-batch)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [CSV for batch results; text for single calculations and run summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch results include converted creatinine and equation provenance; eGFR values are rounded to one decimal place.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
