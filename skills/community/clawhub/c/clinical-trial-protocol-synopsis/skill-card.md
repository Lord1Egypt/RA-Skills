## Description:

Helps clinical investigators, sponsor medical writers, and study teams convert an investigator concept or target-product-profile note into a draft ICH E6(R3) / ICH M11-aligned protocol synopsis with PICOT, estimands, eligibility criteria, statistical considerations, and sponsor and IRB review questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

External clinical investigators, sponsor medical writers, and study teams use this skill to structure an investigator concept or sponsor target product profile into a draft protocol synopsis for sponsor medical, biostatistics, regulatory, pharmacovigilance, and IRB / IEC review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Draft protocol synopsis output may be mistaken for a final protocol, medical decision, regulatory submission, or IRB / IEC communication.

Mitigation: Keep the draft sponsor-review label on outputs and require sponsor medical, biostatistics, regulatory, pharmacovigilance, and IRB / IEC review before use.

Risk: Clinical facts, dose or regimen details, safety signals, or effect-size assumptions may be incomplete or unsourced.

Mitigation: Require source tags, mark unsupported values as Unknown, and verify against literature, label / SmPC, sponsor TPP, investigator brochure, and biostatistics review.

Risk: Sponsor, patient, or biomarker data may be confidential.

Mitigation: Treat inputs as confidential, avoid external services, and summarize confidential documents by document name and version rather than copying them verbatim.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/clinical-trial-protocol-synopsis)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown draft synopsis with structured sections, tables, open questions, evidence matrix, regulatory and ethics flags, and reviewer sign-off checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-only output with source tags and sponsor / IRB review notice.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
