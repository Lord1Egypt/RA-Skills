## Description:

Helps diagnose slow or failed USB-C charging by comparing a device, charger, and cable and identifying the charging bottleneck.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Consumers and support staff can compare USB-C charger, cable, and device capabilities to identify why charging is slow or failing and what to check before replacing equipment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Charging verdicts may not match a particular device or cable and should not determine safety-critical charging decisions alone.

Mitigation: Confirm actual hardware labels, certification markings, and manufacturer specifications before relying on a verdict.

## Reference(s):

- [USB-C Power Delivery rules](references/pd-rules.md)
- [ClawHub skill listing](https://clawhub.ai/voronindenis5/skills/charger-cable-gate)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Charging verdicts: OK, CAPPED, SLOW, or NO-CHARGE, with the likely bottleneck.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
