## Description:

Build face detection, face landmark detection, face recognition, face expression (emotion) recognition, and age/gender estimation with the face-api.js library (browser or Node.js).

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build browser or Node.js workflows for face detection, landmarks, descriptors, face matching, expression classification, age and gender estimation, and canvas overlays.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Face recognition, webcam capture, emotion classification, and age or gender estimation can involve sensitive biometric processing.

Mitigation: Add clear notice and consent flows, avoid covert identification, minimize retention of face descriptors or webcam data, and check applicable biometric privacy and anti-discrimination requirements before product use.

Risk: Example code can be reused in contexts that identify people or analyze protected traits without enough review.

Mitigation: Require human review of intended use, data handling, and user-facing disclosures before deploying workflows built from the skill.

## Reference(s):

- [API Reference](references/api-reference.md)
- [Examples](references/examples.md)
- [Models Reference](references/models.md)
- [face-api.js repository](https://github.com/justadudewhohacks/face-api.js)
- [face-api.js weights](https://github.com/justadudewhohacks/face-api.js/tree/master/weights)
- [Vlad Mandic face-api model CDN](https://cdn.jsdelivr.net/npm/@vladmandic/face-api/model/)
- [Yeephycho TensorFlow face detection](https://github.com/yeephycho/tensorflow-face-detection)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with inline JavaScript, TypeScript, HTML, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model-selection guidance, setup commands, API usage examples, and privacy-sensitive implementation cautions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
