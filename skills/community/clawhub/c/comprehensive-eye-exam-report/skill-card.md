## Description:

Drafts a structured, AOA-aligned comprehensive eye exam report from optometry encounter data for licensed Doctor of Optometry review before prescription issuance or medical record entry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Doctors of Optometry, optometric residents, and clinical documentation specialists use this skill to turn encounter findings into a structured draft comprehensive eye exam report. It supports visual acuity, refraction, binocular vision, anterior and posterior segment findings, IOP, ancillary testing, diagnoses, referral flags, and treatment planning for OD review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Draft clinical documentation could be mistaken for a finalized eye exam report or clinical decision.

Mitigation: Keep outputs labeled as drafts and require licensed Doctor of Optometry review and signature before prescription issuance, medical record entry, billing, referral, or related clinical use.

Risk: Patient identifiers or unnecessary sensitive information could be entered during report drafting.

Mitigation: Use initials and year of birth only, and avoid full names, full dates of birth, MRNs, insurance numbers, and other unnecessary patient identifiers.

Risk: Diagnosis codes, referral flags, or plan language may be incomplete or require clinician confirmation.

Mitigation: Require the OD to confirm ICD-10 codes, review all flagged findings, and document a plan or clinical rationale before finalizing the report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/comprehensive-eye-exam-report)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Structured Markdown draft report with tables, flagged issues, open items, and a licensed OD review signature block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft documentation only; requires licensed OD review before use in prescriptions, medical records, billing, referrals, or related clinical workflows.]

## Skill Version(s):

0.1.0 (source: server release metadata and changelog, released 2026-06-01)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
