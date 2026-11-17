## Description:

RAG-enhanced compliance Q&A with regulatory interpretation guardrails, source attribution, and escalation triggers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dangsllc](https://clawhub.ai/user/dangsllc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, compliance teams, and other authorized users use this skill to answer compliance questions from user-provided documents with citations, caveats, confidence labels, and escalation triggers. It is intended as document-grounded assistance and not as legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read sensitive compliance documents supplied by the user.

Mitigation: Provide only documents needed for the question and avoid sharing unrelated or unnecessary sensitive material.

Risk: Users may over-rely on outputs for legal or compliance decisions.

Mitigation: Treat responses as document-grounded assistance, not legal advice, and route active incidents or critical non-compliance questions to qualified human review.

Risk: Insufficient or conflicting source context can lead to incomplete answers.

Mitigation: Require citations, explicit context gaps, confidence labels, and escalation when the provided documents do not support a clear answer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dangsllc/skills/compliance-qa)
- [Publisher profile](https://clawhub.ai/user/dangsllc)
- [Rote Compliance Skills](https://github.com/Rote-Compliance/rote-compliance-skills)
- [Rote Compliance](https://rotecompliance.com)
- [Dang's Solutions](https://dangssolutions.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown with cited summary, detailed analysis, context gaps, confidence, and escalation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Grounded in user-provided compliance documents; not legal advice.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
