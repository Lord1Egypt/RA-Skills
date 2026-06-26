## Description: <br>
Use when building or reviewing Canvas 2D, Three.js/WebGL, React Three Fiber, GLSL shaders, ShaderToy-to-WebGL adaptation, 2D/3D visualization, game rendering, animation loops, GPU resource cleanup, or rendering performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bovinphang](https://clawhub.ai/user/bovinphang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to implement or review browser-based 2D and 3D rendering work with Canvas, Three.js/WebGL, React Three Fiber, GLSL shaders, animation loops, responsive rendering, accessibility fallbacks, and GPU resource cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Canvas and WebGL content may be inaccessible to screen readers or keyboard-only users. <br>
Mitigation: Provide aria labels, alternative text or DOM summaries, and keyboard-accessible paths for interactive graphics. <br>
Risk: Unbounded DPR, large textures, complex shaders, or undisposed Three.js resources can overload devices or leak GPU memory. <br>
Mitigation: Cap pixel ratio, geometry, texture sizes, shader steps, and particle counts; pause unused animation loops and dispose geometry, materials, textures, controls, and renderers on cleanup. <br>
Risk: Shader or resize mistakes can leave the canvas blank, stretched, or failing only in specific viewports. <br>
Mitigation: Verify desktop and mobile rendering, update draw buffers, viewports, cameras, and uniforms on resize, and check that shader compile and link logs are clean. <br>


## Reference(s): <br>
- [Canvas, Three.js, and R3F patterns](references/rendering-patterns.md) <br>
- [Shader and WebGL patterns](references/shader-webgl-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration, markdown] <br>
**Output Format:** [Markdown guidance with TypeScript, TSX, WebGL, and GLSL code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on responsive canvas sizing, animation loops, shader adaptation, accessibility alternatives, performance budgets, and cleanup checks.] <br>

## Skill Version(s): <br>
2.5.0 (source: server release evidence, README.md, metadata.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
