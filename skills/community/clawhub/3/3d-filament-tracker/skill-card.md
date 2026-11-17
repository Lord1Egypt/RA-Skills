## Description:

3D Filament Tracker turns 3D printing filament order screenshots into a single-file interactive HTML inventory tracker with material, color, roll count, localStorage state, and JSON import/export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heavenchenggong](https://clawhub.ai/user/heavenchenggong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to review 3D printing filament order screenshots, confirm extracted material, color, and roll-count data, and generate a local browser-based inventory tracker with state backup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screenshot-derived order text may include untrusted seller or order data that is inserted into executable HTML.

Mitigation: Require HTML escaping, strict data-id validation, and safe DOM construction before generating or opening the tracker.

Risk: Order screenshots can contain private purchase information.

Mitigation: Warn users to review screenshots before processing and avoid using screenshots from other people or untrusted sources without consent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/heavenchenggong/skills/3d-filament-tracker)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [HTML tracker template](artifact/templates/template.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Guidance]

**Output Format:** [Markdown confirmation table plus generated single-file HTML and JSON state data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses localStorage for browser persistence and JSON import/export for moving or restoring tracker state.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
