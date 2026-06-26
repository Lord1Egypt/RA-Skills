## Description: <br>
CSS animation adapter patterns for HyperFrames. Use when authoring CSS keyframes, animation-delay based timing, animation-fill-mode, animation-play-state, or CSS-only motion that HyperFrames must seek deterministically during preview and rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucas-kay8](https://clawhub.ai/user/lucas-kay8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to author HyperFrames CSS keyframe animations that can be previewed and rendered deterministically. It helps choose CSS timing, fill mode, data attributes, and validation steps for simple decorative or one-element motion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CSS-only motion may fail deterministic rendering if it depends on infinite animations, wall-clock JavaScript, user-triggered state, or layout-changing properties. <br>
Mitigation: Use finite durations and iteration counts, data timing attributes, animation-fill-mode: both, transform-based motion, and the documented HyperFrames validation commands. <br>
Risk: The suggested validation commands run local project tooling and may depend on the user's installed HyperFrames environment. <br>
Mitigation: Review the commands before running them and execute them only in a trusted project workspace. <br>


## Reference(s): <br>
- [MDN CSS animation documentation](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation) <br>
- [MDN animation-fill-mode](https://developer.mozilla.org/en-US/docs/Web/CSS/animation-fill-mode) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands] <br>
**Output Format:** [Markdown with HTML, CSS, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
