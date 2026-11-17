## Description:

Helps an agent plan and check a video previz with storyboards, Three.js, or Blender, then prepare the result for a video model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video creators use this skill to plan and check camera, blocking, timing, and continuity before generating a video. It helps them choose an appropriate prototype, from storyboard stills to a 3D scene, and prepare a handoff to a video model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A preview server with network access may expose scene files to other clients.

Mitigation: Review the preview server settings and restrict access to trusted clients before opening it on a network.

Risk: Sending footage or other materials to video model providers may disclose content outside the user's environment.

Mitigation: Check what each provider will receive and confirm that sharing the material is approved before submitting it.

Risk: The security review notes an install-command concern and partial analysis of two scripts, so behavior is not fully assessed.

Mitigation: Review installation commands and inspect the incompletely analyzed scripts before running or installing related components.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vargai/skills/code-to-video-previz)
- [How to make a video with an AI agent in ten steps](https://varg.ai/how-to/make-a-video-in-ten-steps)
- [Previz a video in Three.js or Blender](https://varg.ai/how-to/previz-a-video-in-threejs-or-blender)
- [Staging format](references/staging-format.md)
- [Reference video workflow](references/reference-video.md)
- [Painting and still workflow](references/paintings.md)
- [Video model handoff](references/handoff.md)
- [Take judging guide](references/judging.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration, Shell commands, Text]

**Output Format:** [Markdown guidance, scene configuration (JSON), Python or TypeScript code, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include staging measurements, rendered frame reviews, and prompts for a video model.]

## Skill Version(s):

1.0.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
