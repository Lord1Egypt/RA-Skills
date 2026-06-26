## Description: <br>
Use this skill when a clinical genomics professional wants to draft or review an ACMG/AMP germline variant-interpretation memo before report sign-out. Covers HGVS validation, ClinGen SVI/VCEP rules, evidence grading, final classification, ClinVar-ready records, and laboratory sign-out boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical genomics professionals use this skill to draft or review an internal ACMG/AMP germline variant-interpretation memo before report sign-out. It supports evidence gathering, rule tracing, draft ClinVar-ready records, downstream action planning, and laboratory director review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users could paste direct patient identifiers or confidential variant and pedigree details into the assistant. <br>
Mitigation: Use pseudonymised case identifiers only; redact names, dates of birth, MRNs, addresses, contact details, photos, and other direct identifiers before use. <br>
Risk: Draft variant interpretations may be incorrect, incomplete, or inappropriate for clinical action without expert review. <br>
Mitigation: Have qualified clinical genomics personnel and a certifying laboratory director review the output before any report, ClinVar submission, or patient-facing action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/archlab-space/acmg-variant-interpretation-memo) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown draft memo with evidence tables, rule trace, ClinVar-ready record, downstream actions, and sign-out block] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft support only; outputs require qualified clinical review and certifying laboratory director sign-out before reporting, submission, or patient-facing use.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata and changelog, released 2026-05-28) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
