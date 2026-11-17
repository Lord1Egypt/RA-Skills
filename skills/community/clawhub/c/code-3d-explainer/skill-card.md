## Description:

Creates 3D explainer videos from code, using sourced facts, part-by-part scenes, camera tours, and checks for labels and on-screen claims.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and science communicators use this skill to create short, fact-checked 3D explainers for subjects that are difficult to film.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports an unauthenticated rendering server with a file exposure risk.

Mitigation: Review the rendering-server exposure and address the affected checks before installing.

Risk: Optional narration uses an external service, and the security guidance notes that confidential scripts could be disclosed.

Mitigation: Do not send confidential scripts to external narration services unless that disclosure is understood and approved.

Risk: The security assessment covered only 16 of 23 components fully, so its evidence is incomplete.

Mitigation: Review the remaining components before relying on the assessment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/vargai/skills/code-3d-explainer)
- [Fact sheet workflow](artifact/references/fact-sheet.md)
- [Build and camera guide](artifact/references/build-and-camera.md)
- [Label checks](artifact/references/labels.md)
- [Example animal-cell film](https://s3.varg.ai/files/4325c578-378d-4c43-ae53-3cc3218df1ea/file_b6dc1bd5642f.mp4)

## Skill Output:

**Output Type(s):** [Video, Code, Markdown, Configuration, Shell commands]

**Output Format:** [MP4 video, Markdown fact sheet, JavaScript or TypeScript source, JSON scene configuration, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video resolution, duration, and subject depend on the project.]

## Skill Version(s):

1.0.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
