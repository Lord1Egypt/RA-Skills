## Description:

Offline contract triage for freelancers that segments NDA, MSA, or SOW text and flags potential intellectual-property, liability, non-compete, and payment concerns across four categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nenadzivotic](https://clawhub.ai/user/nenadzivotic)

### License/Terms of Use:

MIT-0

## Use Case:

Freelancers can use this skill to review a contract before signing, identify clauses that merit closer attention, and spot missing protections. It is preliminary triage, not legal advice or a complete review of all contract risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The lite checker covers only four of ten contract-risk categories, so it may miss important issues.

Mitigation: Use results as limited triage, verify flagged clauses in the original document, and seek qualified legal review for material exposure or a complete assessment.

Risk: An unreviewed installer or repository revision may not match the intended release.

Mitigation: Use a reviewed installer version and repository revision.

Risk: Offline helper behavior does not determine the hosting agent's model privacy, and marketplace actions may involve network access.

Mitigation: For strictly offline operation, use the local helper and disable marketplace actions; assess the hosting agent's model privacy separately.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/nenadzivotic/skills/contract-triage-lite)
- [Publisher profile](https://clawhub.ai/user/nenadzivotic)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured JSON triage report with a concise text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports clause flags, severity counts, missing payment or liability protections, and an upgrade hint when relevant; evaluates four of ten risk categories.]

## Skill Version(s):

1.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
