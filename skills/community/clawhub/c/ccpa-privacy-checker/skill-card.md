## Description:

Assess your business's compliance with California Consumer Privacy Act (CCPA) regulations and identify privacy governance gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Compliance, privacy, and legal teams use this skill to evaluate CCPA readiness across business practices, data handling, consumer rights workflows, disclosures, vendor controls, and governance processes. It returns a compliance score, critical gaps, risk assessment, and remediation recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-provided business privacy and compliance details to a third-party API.

Mitigation: Submit only the assessment fields needed for the CCPA review and avoid unnecessary regulated, customer-specific, or confidential records.

Risk: Compliance scores and remediation estimates may be incomplete or unsuitable as final legal advice.

Mitigation: Have privacy, compliance, or legal reviewers validate findings before relying on the output for regulatory decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/ccpa-privacy-checker)
- [OpenAPI specification](artifact/openapi.json)
- [API documentation](https://api.mkkpro.com:8040/docs)
- [CCPA compliance API route](https://api.mkkpro.com/compliance/ccpa-privacy)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, API calls]

**Output Format:** [Markdown guidance with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces compliance scores, gap analysis, risk estimates, and prioritized remediation recommendations from user-provided business privacy details.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
