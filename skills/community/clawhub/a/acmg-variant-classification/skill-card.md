## Description: <br>
Standard workflow for ACMG/AMP germline small-variant classification: collect evidence, assign criteria, detect conflicts, and produce a review-ready classification summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alex4xu](https://clawhub.ai/user/alex4xu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical genetics reviewers, laboratory staff, and developers use this skill to guide ACMG/AMP-style interpretation of germline SNVs and indels. It collects variant, phenotype, inheritance, population, functional, database, and literature evidence, then helps produce a provisional review-ready classification summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow handles sensitive clinical and genetic information. <br>
Mitigation: Avoid unnecessary patient identifiers and keep any generated records in approved clinical storage. <br>
Risk: ACMG criteria or gene-specific guidance may be misapplied, producing misleading decision support. <br>
Mitigation: Validate criteria against current ACMG/AMP and ClinGen guidance and require expert manual review before relying on outputs. <br>


## Reference(s): <br>
- [ACMG Variant Classification SOP](references/sop.md) <br>
- [Bundled classifier test cases](references/test_cases.json) <br>
- [Variant intake template](templates/intake.md) <br>
- [Evidence table template](templates/evidence-table.md) <br>
- [ClawHub skill page](https://clawhub.ai/alex4xu/acmg-variant-classification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Guided prose and markdown tables, with optional shell commands for the bundled classifier script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Decision-support output only; final classification requires expert manual review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
