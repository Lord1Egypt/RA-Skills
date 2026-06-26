## Description: <br>
Guides contributors through planning, scaffolding, building, validating, previewing, and submitting a HyperFrames registry block or component as an upstream pull request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucas-kay8](https://clawhub.ai/user/lucas-kay8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External contributors and developers use this skill when they want to add a new public HyperFrames catalog block or component, such as a caption style, VFX block, transition, lower third, text effect, overlay, or snippet. It walks them from intent clarification through validation, preview publishing, and PR creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow includes publishing previews, pushing branches, opening pull requests, and optionally uploading catalog images. <br>
Mitigation: Review generated files and preview assets for sensitive content, confirm remote targets, and run publish, upload, push, and PR commands only after explicit user approval. <br>
Risk: The AWS catalog-image upload path is intended only for authorized HeyGen internal contributors. <br>
Mitigation: Use the AWS upload step only with authorized internal credentials; external contributors should attach the preview MP4 to the pull request for maintainer handling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lucas-kay8/contribute-catalog) <br>
- [HyperFrames registry item schema](https://hyperframes.heygen.com/schema/registry-item.json) <br>
- [GSAP distribution](https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js) <br>
- [Google Fonts Montserrat stylesheet](https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&display=swap) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline JSON, HTML, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces contribution instructions and starter templates; generated project files and external publishing actions require user review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
