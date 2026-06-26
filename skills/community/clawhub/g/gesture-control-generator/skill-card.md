## Description: <br>
Generates complete browser-based HTML scenes that let users control Three.js visual effects with either mouse input or webcam-based hand gestures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouchang1988](https://clawhub.ai/user/zhouchang1988) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and creative technologists use this skill to generate self-contained interactive HTML visual effects, including particles, butterflies, ripples, fireworks, stars, and other custom scenes controlled by mouse or hand gestures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated pages can request webcam access for gesture control. <br>
Mitigation: Prefer mouse-only mode when camera access is unnecessary, and review or modify generated pages so camera startup occurs only after an explicit user action. <br>
Risk: Generated pages load Three.js and MediaPipe code from jsDelivr. <br>
Mitigation: Review remote script dependencies before deployment and pin or self-host approved copies when operating in controlled environments. <br>
Risk: Generated file paths and support-file copies may place new HTML or JavaScript files in the workspace. <br>
Mitigation: Review proposed output paths before allowing file creation and scan generated files before sharing or deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhouchang1988/gesture-control-generator) <br>
- [particles.html](references/particles.html) <br>
- [butterfly.html](references/butterfly.html) <br>
- [ripple.html](references/ripple.html) <br>
- [Three.js CDN dependency](https://cdn.jsdelivr.net/npm/three@0.149.0/build/three.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTML, JavaScript, and configuration snippets; generated usage may create complete HTML files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated pages may include Three.js rendering, local gesture-scene.js support code, browser camera controls, and remote CDN script dependencies.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata; artifact SKILL.md frontmatter lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
