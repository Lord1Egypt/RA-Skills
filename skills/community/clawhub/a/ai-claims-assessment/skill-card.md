## Description:

Assesses public healthcare-AI vendor documents to identify gaps between AI use claims, legal language, and HIPAA rules on PHI handling and model training.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dangsllc](https://clawhub.ai/user/dangsllc)

### License/Terms of Use:

MIT-0

## Use Case:

Healthcare compliance, legal, and vendor-risk reviewers use this skill to assess public healthcare-AI vendor marketing pages, Terms of Service, and Privacy Policies against included HIPAA reference text. It produces cited public-documentation gaps for qualified human review, without asserting actual PHI mishandling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill could be applied to private patient records or confidential business associate agreements outside its intended public-document scope.

Mitigation: Install and use it only for public vendor documentation, not private PHI, patient records, or confidential BAAs.

Risk: Compliance-analysis output could be treated as a final vendor decision or legal conclusion.

Mitigation: Require review by a qualified human before relying on the findings for vendor decisions.

Risk: Readers may overstate public-documentation gaps as evidence of actual PHI mishandling.

Mitigation: Frame findings as gaps visible in public materials and avoid claims about actual vendor handling of PHI.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dangsllc/skills/ai-claims-assessment)
- [Publisher profile](https://clawhub.ai/user/dangsllc)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown guidance with a JSON-shaped gap map]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only analysis of provided public documents; no external retrieval.]

## Skill Version(s):

1.0.1 (source: server release metadata, created 2026-07-20)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
