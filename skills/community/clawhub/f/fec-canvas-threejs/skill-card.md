## Description:

Guides developers building and reviewing Canvas 2D, Three.js/WebGL, React Three Fiber, and shader-based browser visuals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bovinphang](https://clawhub.ai/user/bovinphang)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to build and review accessible, responsive browser graphics, including 2D/3D scenes, shaders, animation loops, and rendering performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Canvas and WebGL visuals may not be accessible to screen readers or keyboard users.

Mitigation: Provide alternative text or a DOM summary and keyboard paths for interactive content.

Risk: Unbounded render loops or unreleased GPU resources can degrade performance.

Mitigation: Limit pixel ratio and rendering complexity, pause or cancel unused loops, and dispose of graphics resources.

Risk: Shader or resize mistakes may produce blank or distorted visuals.

Mitigation: Check shader compilation logs and visually verify canvas size and output across device sizes.

## Reference(s):

- [Canvas, Three.js and R3F patterns](references/rendering-patterns.md)
- [Shader and WebGL patterns](references/shader-webgl-patterns.md)
- [Frontend Craft project homepage](https://github.com/bovinphang/frontend-craft)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration instructions]

**Output Format:** [Markdown with TypeScript and GLSL guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rendering and visual verification recommendations]

## Skill Version(s):

2.9.0 (source: ClawHub release, README.md, metadata.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
