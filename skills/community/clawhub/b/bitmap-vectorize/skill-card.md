## Description: <br>
Converts bitmap images such as screenshots, hand-drawn photos, and schematic diagrams into precise SVG or HTML Canvas vector graphic code, especially for physics diagrams, geometry figures, circuit diagrams, and annotated images that require accurate reconstruction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wxdwqy](https://clawhub.ai/user/wxdwqy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, educators, and content creators use this skill to recreate user-provided physics or schematic-style bitmap diagrams as editable Canvas or SVG code. It guides the agent through identifying diagram elements, checking them with the problem text, generating vector graphics, and reviewing the result with the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated diagram code may misrepresent the source image or physics problem if image details are ambiguous. <br>
Mitigation: Use the skill's required user verification steps to confirm identified components, positions, relationships, labels, and visual details before using the output. <br>
Risk: Generated Canvas or SVG code may be unsuitable for direct use in a webpage or shared document without review. <br>
Mitigation: Review and scan generated code before publishing, embedding, or sharing it. <br>
Risk: The workflow is mainly tailored to physics and schematic-style diagrams, so results for logos, photographs, or arbitrary screenshots may be uneven. <br>
Mitigation: Prefer this skill for physics or schematic diagrams and verify outputs carefully for other image types. <br>


## Reference(s): <br>
- [Physics Shapes Reference](references/physics_shapes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown guidance with HTML Canvas or SVG code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output is HTML Canvas code; SVG and PNG export are optional when requested by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
