## Description:

Pet Camera Vision captures camera frames, prepares multimodal analysis prompts, and normalizes face presence, emotion, and dominant colors into structured JSON for desktop-pet memory and feedback workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lizy022868](https://clawhub.ai/user/lizy022868)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building OpenClaw desktop-pet companions use this skill to capture webcam or camera images and convert local or model-assisted vision analysis into structured state for memory, emotion analysis, and feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can capture camera snapshots and save raw images locally.

Mitigation: Enable visible capture indicators, require explicit user consent before capture, and define retention and deletion rules for saved images.

Risk: The skill infers face presence and emotion from camera images.

Mitigation: Use the inferred emotion state as a low-confidence signal, avoid high-stakes decisions, and allow users to disable emotion analysis.

Risk: The security scan notes missing consent, retention, and deletion controls.

Mitigation: Add consent and disablement flows before using the skill around other people or in shared spaces.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lizy022868/skills/deskpet-skills)
- [Vision analysis prompt](artifact/prompts/analyze_vision.md)
- [Demo workflow](artifact/examples/demo.md)
- [Example normalized output](artifact/examples/example_output.json)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, files]

**Output Format:** [Single-line JSON, plain-text multimodal prompts, and saved JPG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normalized output includes presence, presence method, emotion, confidence, dominant colors, image path, and timestamp.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
