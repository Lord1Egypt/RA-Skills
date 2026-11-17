## Description:

Use when clothes take multiple cycles to dry, the laundry room is hot/humid, or you want to audit a dryer vent for lint buildup and fire risk. Computes vent equivalent length vs code max, dry-time creep diagnosis, and a clean/replace/repair ladder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Homeowners and household maintainers use this skill to assess slow drying and visible dryer vent conditions, estimate whether a vent run exceeds the stated length allowance, and plan cleaning, duct replacement, or professional inspection. It supports maintenance decisions and does not replace an on-site inspection.

### Deployment Geography for Use:

United States (the guidance uses IRC M1502 assumptions)

## Known Risks and Mitigations:

Risk: The testing sequence or conflicting vent calculations could lead to unsafe conclusions.

Mitigation: Have corrected testing steps and vent-length calculations checked against the appliance manual before relying on results.

Risk: Testing or continuing to use the dryer with warning signs could be unsafe.

Mitigation: Do not run the drying test with unexplained overheating, a burning smell, or a previous thermal shutdown; arrange inspection before reuse. If fire is suspected, leave and contact emergency services.

Risk: Gas-line work can create additional hazards.

Mitigation: Follow the appliance manual and use a qualified technician for gas-line work.

## Reference(s):

- [Vent code and fire model reference](artifact/references/vent-code-and-fire-model.md)
- [ClawHub release](https://clawhub.ai/voronindenis5/skills/dryer-vent-fire-guard)

## Skill Output:

**Output Type(s):** [Guidance, Text, JSON, Shell commands]

**Output Format:** [Markdown guidance and audit results, with optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline audit based on user-entered vent details and dry-time observations; it cannot inspect the vent physically.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
