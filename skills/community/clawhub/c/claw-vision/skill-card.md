## Description:

Analyze local images with a Gemini 3.1 Pro Preview (NUWA Flux) helper, including screenshots, receipts, UI, documents, and photos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[puma1981](https://clawhub.ai/user/puma1981)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route local image files to a vision-analysis helper and receive structured summaries, extracted fields, UI element lists, and confidence labels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected local images may be sent to an external Gemini/NUWA vision service.

Mitigation: Use the skill only for images whose contents can be disclosed to that service; avoid sensitive screenshots, receipts, documents, or photos unless that disclosure is acceptable.

Risk: The skill depends on a local vision-tool.py helper script that is outside the reviewed package.

Mitigation: Review and verify the local helper script before enabling the skill in an agent environment.

## Reference(s):

- [Claw Vision on ClawHub](https://clawhub.ai/puma1981/skills/claw-vision)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Structured plain text with summary, fields, UI elements, and confidence sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Consumes a local image path and prompt; URL image inputs are not supported by the skill artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
