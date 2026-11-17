## Description:

Generates gesture-controlled interactive scenes by asking what the user wants to control, then producing a complete HTML file that supports mouse and camera-based gesture input.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouchang1988](https://clawhub.ai/user/zhouchang1988)

### License/Terms of Use:

MIT

## Use Case:

Developers and creators use this skill to generate browser-based visual effects that respond to mouse movement or webcam-powered hand gestures. It is suited for interactive demos, creative coding prototypes, and lightweight web experiences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated pages can request and start webcam use on page load while running external CDN scripts.

Mitigation: Review generated files before opening them, prefer mouse-only mode when camera use is not required, and avoid running them in sensitive camera contexts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhouchang1988/skills/gesture-control-generator)
- [Particle trail example](references/particles.html)
- [Butterfly example](references/butterfly.html)
- [Ripple example](references/ripple.html)
- [Three.js CDN dependency](https://cdn.jsdelivr.net/npm/three@0.149.0/build/three.min.js)

## Skill Output:

**Output Type(s):** [code, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML, JavaScript, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated HTML pages depend on a local gesture-scene.js helper and browser support for camera permission when gesture mode is used.]

## Skill Version(s):

1.2.0 (source: server release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
