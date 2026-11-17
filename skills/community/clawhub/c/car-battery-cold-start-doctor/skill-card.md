## Description:

Helps diagnose cold-weather starting problems in 12 V lead-acid batteries using voltage, temperature, age, and rated CCA, with failure-triage and jump-start guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Drivers and vehicle owners use this skill to assess a 12 V lead-acid battery before winter or after slow or failed starts, and to distinguish likely battery problems from starter, alternator, or parasitic-drain issues. It provides estimates and basic roadside guidance from user-entered measurements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic predictions are rough estimates and may not reflect a battery's actual condition.

Mitigation: Confirm replacement decisions with a battery test.

Risk: Jump-start procedures vary by vehicle and an incorrect procedure can be unsafe.

Mitigation: Follow the vehicle manual for jump-start procedures.

## Reference(s):

- [Battery physics and failure signatures](references/battery-physics.md)
- [ClawHub release page](https://clawhub.ai/voronindenis5/skills/car-battery-cold-start-doctor)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, JSON]

**Output Format:** [Plain-text or JSON diagnostic report with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Estimates depend on user-entered battery measurements and vehicle details.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
