## Description: <br>
Use when the user wants an OpenClaw agent to choose the right CleanShot Tool plugin call for screenshots, OCR, screen recording, scrolling capture, annotation, pinned references, CleanShot history, Quick Access, or settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lyzmin41](https://clawhub.ai/user/lyzmin41) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and developers use this skill to guide an agent in selecting CleanShot Tool plugin actions for screenshots, OCR, screen recording, scrolling capture, annotation, pinned references, history, Quick Access, and settings workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screen capture, OCR, recording, and history workflows can expose visible passwords, private chats, documents, or other sensitive content. <br>
Mitigation: Use the skill only when intended content is visible; avoid invoking it while sensitive material is onscreen, and prefer local copy or save unless the user explicitly requests upload. <br>
Risk: Some CleanShot actions may open UI flows or require user confirmation rather than completing entirely through the agent. <br>
Mitigation: State when CleanShot UI confirmation is required, avoid claiming an image was sent or recording started unless the environment confirms it, and fall back to manual area selection when display geometry is uncertain. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lyzmin41/cleanshot-skill) <br>
- [README](README.md) <br>
- [Examples](examples.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, tool-call parameters] <br>
**Output Format:** [Markdown guidance with CleanShot Tool plugin names, modes, actions, and parameter choices] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; assumes the CleanShot Tool plugin, macOS, CleanShot X, and the CleanShot X API are available.] <br>

## Skill Version(s): <br>
0.2.0 (source: package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
