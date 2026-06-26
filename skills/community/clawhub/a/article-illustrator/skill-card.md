## Description: <br>
Analyzes article structure, identifies where visuals add value, and helps an agent generate content-grounded illustrations using a Type x Style framework. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External writers, editors, and content teams use this skill to add structured illustrations to articles or blog posts. It helps choose illustration type, density, and style, then produces an outline, image prompts, generated images, and Markdown image references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Article drafts and derived image prompts may contain private or sensitive content that is sent to an image generator. <br>
Mitigation: Use approved image-generation services, review prompts before submission, and avoid sending sensitive drafts unless the environment is authorized for that content. <br>
Risk: Generated illustrations may raise copyright, likeness, or sensitive-subject concerns, especially where the artifact asks not to refuse certain requests. <br>
Mitigation: Treat platform safety, copyright, and privacy policies as higher priority than the skill text, and review outputs involving real people, copyrighted characters, or sensitive subjects. <br>
Risk: Updating an original article or overwriting existing images can cause unwanted content changes. <br>
Mitigation: Prefer an illustrated-copy output for important files and confirm supplement, overwrite, or regenerate choices before changing existing assets. <br>


## Reference(s): <br>
- [Article Illustrator ClawHub Page](https://clawhub.ai/wpank/article-illustrator) <br>
- [Usage](references/usage.md) <br>
- [Style Reference](references/styles.md) <br>
- [Prompt Construction](references/prompt-construction.md) <br>
- [Preferences Schema](references/config/preferences-schema.md) <br>
- [First-Time Setup](references/config/first-time-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Image prompts, Images, Configuration guidance] <br>
**Output Format:** [Markdown files, prompt files, image files, and inline Markdown image references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates an outline, per-illustration prompts, and generated image files in a user-selected output directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
