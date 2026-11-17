## Description:

Helps households inventory home, car, or travel first-aid kits, identify expired or missing supplies, and prioritize restocking for their needs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT-0

## Use Case:

Households and caregivers use this skill to assess first-aid kit supplies against household needs, track expiration dates, and prepare restocking lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Household conditions and kit inventory are stored in a plaintext local JSON registry.

Mitigation: Choose a private location with --db and restrict access to the registry.

Risk: A stock audit could be mistaken for medical advice or emergency guidance.

Mitigation: Use it only to plan supplies; seek clinician advice for prescriptions and call local emergency services in an emergency.

## Reference(s):

- [First-Aid Kit Auditor on ClawHub](https://clawhub.ai/voronindenis5/skills/first-aid-kit-auditor)
- [Catalog rationale](artifact/references/catalog-rationale.md)
- [Storage and rotation](artifact/references/storage-and-rotation.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain-text inventory summaries and prioritized shopping lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coverage percentage, expiration and stock alerts, and a readiness verdict.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
