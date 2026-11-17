## Description:

Analyzes Tomato novel IP content to extract worldbuilding, character settings, core conflicts, highlight points, and an initial compliance result for short-drama adaptation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ghwyever](https://clawhub.ai/user/ghwyever)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to turn Tomato novel text into structured IP analysis for AI short-drama adaptation. It is intended for extracting story facts and creative planning signals, not for final content moderation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends full novel text and the configured API key to an external endpoint.

Mitigation: Use only non-sensitive novel text and a trusted HTTPS API endpoint that you control.

Risk: The compliance_check result should not be treated as reliable final moderation because the inspected code always marks content as safe.

Mitigation: Run independent content review or a dedicated moderation workflow before relying on compliance conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ghwyever/skills/01-tomato-ip-parse)
- [Artifact SKILL.md](artifact/SKILL.md)
- [Artifact manifest.json](artifact/manifest.json)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON object containing structured IP information and a compliance_check object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires API_KEY, API_BASE, and MODEL_NAME configuration for the external model endpoint.]

## Skill Version(s):

1.0.5 (source: server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
