## Description:

Guides homeowners through safety-first furnace troubleshooting, distinguishes simple checks from situations requiring a professional, and prepares a technician briefing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT-0

## Use Case:

Homeowners, renters, and landlords use this skill to triage heating failures, identify when to stop and seek emergency help, try basic checks when safe, and prepare details for an HVAC technician.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The thermostat jumper instruction could expose a homeowner to electrical or equipment hazards if applied to the wrong circuit.

Mitigation: Avoid the jumper step unless a qualified person confirms a low-voltage conventional thermostat circuit and uses proper precautions.

Risk: The helper may write furnace incident details to ~/.furnace_log.json by default.

Mitigation: Use --no-log when a local record is not wanted; review and protect any log that is created.

Risk: Troubleshooting guidance can delay appropriate emergency response to carbon monoxide, fuel leaks, smoke, or electrical burning.

Mitigation: Treat the skill as decision support only; stop diagnostics and follow emergency guidance when danger signs appear.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/voronindenis5/skills/furnace-panic-doctor)
- [Diagnostic tree](references/diagnostic-tree.md)
- [Symptom table](references/symptom-table.md)
- [Manuals and error codes](references/manuals-and-codes.md)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain-text diagnostic verdict, suggested next steps, and optional technician briefing]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local JSON incident log unless --no-log is used.]

## Skill Version(s):

1.0.1 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
