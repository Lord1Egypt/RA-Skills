## Description:

Queries ArkCLI resources visible to the current or selected profile and resolves endpoint bindings, modalities, and supported workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonstarlight](https://clawhub.ai/user/jasonstarlight)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect profile-visible endpoints or plan models, assess profile compatibility, and identify a suitable workflow for a supplied endpoint. It reports discovery metadata and does not guarantee a successful API call.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Static image and video catalog entries may not reflect current resource availability.

Mitigation: Confirm availability with a current ArkCLI resources query before relying on an entry.

Risk: Security inspection was partial because two local references were unavailable to the scan.

Mitigation: Review the referenced materials before relying on guidance that depends on them.

## Reference(s):

- [Resource List Reference](artifact/references/arkcli-resources-list.md)
- [ClawHub Release](https://clawhub.ai/jasonstarlight/skills/arkcli-resources)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON with concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only resource discovery; this skill does not create, modify, or delete resources.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
