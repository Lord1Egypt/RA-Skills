## Description:

AI桌面宠物 is a browser-based 3D desktop pet with emotion detection, letting an interactive dog or cat react to mood text, actions, and uploaded pet photos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to open or embed a static browser-based 3D dog/cat companion that responds to Chinese emotion keywords, manual pet actions, and photo-derived colors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The browser UI loads Three.js from the unpkg CDN.

Mitigation: Use the skill in environments where that CDN dependency is acceptable, or pin and host the dependency internally for controlled deployments.

Risk: Photo color extraction and emotion keyword input may involve personal images or mood text, and the current UX is Chinese-focused.

Mitigation: Tell users what local browser processing is expected, avoid sensitive inputs, and verify the language behavior fits the intended audience.

Risk: WebGL, local-file image handling, and floating-window mode can be restricted by browser settings.

Mitigation: Run the skill in a modern browser, serve it over HTTP when local file access causes limits, and allow popups only when floating mode is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/ai-desktop-pet)
- [Three.js 0.157 CDN dependency](https://unpkg.com/three@0.157.0/build/three.module.js)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline shell and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static browser UI backed by a local HTML file and optional JavaScript petAPI calls.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
