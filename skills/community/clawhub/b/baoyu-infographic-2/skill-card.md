## Description: <br>
Generates professional infographics with 21 layout types and 20 visual styles by analyzing content, recommending layout and style combinations, and preparing publication-ready infographic assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nengnengZ](https://clawhub.ai/user/nengnengZ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content creators use this skill to turn source material into structured infographic plans, prompts, and generated infographic images with selectable layouts, styles, aspect ratios, and languages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and renames files under an infographic output folder. <br>
Mitigation: Run it in an intended workspace and review output paths before approving file creation or backup operations. <br>
Risk: Source content may be copied into analysis, structured content, and image-generation prompts. <br>
Mitigation: Remove secrets, credentials, and sensitive documents from source material, and review generated prompts before sending them to an image generation tool. <br>
Risk: Optional preference files can alter layout, style, aspect ratio, language, or custom style behavior. <br>
Mitigation: Review project and user EXTEND.md preference files when reproducibility or policy compliance matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nengnengZ/baoyu-infographic-2) <br>
- [Publisher profile](https://clawhub.ai/user/nengnengZ) <br>
- [Homepage from clawdis metadata](https://github.com/JimLiu/baoyu-skills#baoyu-infographic) <br>
- [Analysis framework](references/analysis-framework.md) <br>
- [Structured content template](references/structured-content-template.md) <br>
- [Base infographic prompt](references/base-prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown analysis and structured-content files, an image-generation prompt, local output paths, and a PNG infographic when image generation is available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates an infographic output folder, backs up prior outputs with timestamps, and can read optional baoyu-infographic EXTEND.md preference files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter declares 1.56.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
