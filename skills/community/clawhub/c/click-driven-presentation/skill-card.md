## Description: <br>
Turns an existing narration script into a click-driven, full-screen Vite and React web presentation that advances one beat per click for live recording. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and content teams use this skill to turn a prepared narration script into a browser-based presentation with click-controlled pacing, planning gates, and scene-by-scene visual guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scaffold writes a local presentation project and can write into an existing directory when forced. <br>
Mitigation: Review the target directory before scaffolding and avoid --force unless intentionally writing into that directory. <br>
Risk: The scaffold installs npm dependencies by default. <br>
Mitigation: Use --no-install to inspect generated files first, then install dependencies from the project directory when ready. <br>
Risk: Generated scenes can drift from the narration if step counts and visual beats are not checked. <br>
Mitigation: Keep each scene's steps array as the source of truth and run the documented scene self-check and typecheck before accepting scenes. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Scene Craft](references/SCENE-CRAFT.md) <br>
- [Steps Spec](references/STEPS-SPEC.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/archlab-space/click-driven-presentation) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance plus generated Vite, React, and TypeScript project files with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a local presentation project; npm install runs by default unless --no-install is used.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
