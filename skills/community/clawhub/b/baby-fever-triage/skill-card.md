## Description:

Helps caregivers assess fever urgency in young children, check warning signs, calculate weight-based medicine doses, track symptoms, and prepare a clinician handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Caregivers of previously healthy children aged 0–5 use this skill for informational fever triage, medication planning, local symptom logging, and a summary to discuss with a clinician. It does not replace medical care or emergency services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A caregiver could delay urgent care by relying on informational triage or dosing output.

Mitigation: Treat the output as decision support only; contact emergency services for urgent symptoms and follow a clinician's advice over the tool.

Risk: The local fever log contains sensitive child-health information that others using a shared computer may access.

Mitigation: Keep fever.json in a private directory and delete it when it is no longer needed.

## Reference(s):

- [Triage rules and dosing reference](references/triage-rules.md)
- [ClawHub skill listing](https://clawhub.ai/voronindenis5/skills/baby-fever-triage)

## Skill Output:

**Output Type(s):** [Text, Guidance, Files]

**Output Format:** [Plain-text triage and dosing results, a clinician handoff summary, and a local JSON fever log]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Informational only; medication volumes require the product concentration. Fever logs remain local unless the user shares them.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
