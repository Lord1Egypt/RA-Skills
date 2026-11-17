## Description:

Use this skill when a DPO, privacy counsel, or controller representative needs to draft a GDPR Article 35 Data Protection Impact Assessment (DPIA), covering threshold determination, EDPB harmonised template sections 0-4, risk scoring, and a DRAFT DPIA with prior-consultation recommendation for DPO review and controller sign-off.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

DPOs, privacy counsel, and controller representatives use this skill to draft a GDPR Article 35 DPIA for a single high-risk processing activity. It structures threshold analysis, processing descriptions, compliance checks, risk scoring, mitigations, residual-risk recommendations, open questions, and DPO/controller review material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may collect confidential privacy, vendor, and architecture information needed to draft a DPIA.

Mitigation: Use category-level descriptions instead of raw personal records, handle draft outputs as confidential, and avoid including data-subject identifiers.

Risk: A draft DPIA may be mistaken for final legal approval or controller sign-off.

Mitigation: Keep the DRAFT FOR DPO REVIEW posture, require DPO/controller review, and do not treat the generated assessment as signed or legally final.

## Reference(s):

- [DPIA Drafter README](artifact/README.md)
- [DPIA Drafter changelog](artifact/CHANGELOG.md)
- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/dpia-drafter)
- [ClawHub publisher profile](https://clawhub.ai/user/archlab-space)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown draft DPIA with structured sections, tables, risk register, open questions, evidence index, and review banner]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output is labelled DRAFT for DPO review and controller sign-off; it should not include data-subject identifiers or raw personal records.]

## Skill Version(s):

0.1.1 (source: evidence release and artifact changelog, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
