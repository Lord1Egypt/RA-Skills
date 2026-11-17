## Description:

Use this skill when a clinical genomics professional wants to draft or review an ACMG/AMP germline variant-interpretation memo before report sign-out; it covers HGVS validation, ClinGen SVI/VCEP rules, evidence grading, final classification, ClinVar-ready records, and laboratory sign-out boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical genomics professionals use this skill to draft or review internal germline variant-interpretation memos before report sign-out. It supports evidence collection, ACMG/AMP rule tracing, draft classification, ClinVar-ready records, and review blocks for qualified laboratory sign-out.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive clinical-genomics drafting can expose direct patient identifiers if users paste unredacted case material.

Mitigation: Use only pseudonymized case identifiers and redact names, dates of birth, MRNs, addresses, phone numbers, emails, IP addresses, and photographs before using the skill.

Risk: Variant evidence, database versions, and classification guidance can be incomplete, outdated, or misapplied in a draft memo.

Mitigation: Independently verify HGVS nomenclature, database versions, variant evidence, ClinGen SVI/VCEP guidance, and final classification before laboratory sign-out.

Risk: Draft outputs could be mistaken for final clinical reports, ClinVar submissions, or patient-facing guidance.

Mitigation: Treat all outputs as drafts requiring qualified laboratory director review and sign-out before clinical reporting, ClinVar submission, or patient communication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/acmg-variant-interpretation-memo)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown draft memo with structured evidence tables and sign-out blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces draft clinical-genomics interpretation content that requires qualified laboratory review before use.]

## Skill Version(s):

0.1.3 (source: server release evidence and changelog, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
