## Description: <br>
Generates professional slide deck images from content, creates outlines with style instructions, then generates individual slide images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimliu](https://clawhub.ai/user/jimliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and business users use this skill to turn source content into shareable slide decks with an outline, per-slide image prompts, generated slide images, and optional PPTX or PDF exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The base prompt includes broad instructions around sensitive or copyrighted subjects. <br>
Mitigation: Audit and edit references/base-prompt.md before installation so image generation follows normal safety, likeness, and copyright restrictions. <br>
Risk: Generated prompts and reference images may be sent to the selected image-generation backend. <br>
Mitigation: Use an approved backend, avoid confidential or sensitive inputs, and review prompt files before generation. <br>
Risk: The skill can execute local Bun scripts to merge generated images into PPTX and PDF files. <br>
Mitigation: Run merge scripts only in trusted workspaces after reviewing generated slide images and prompt notes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jimliu/baoyu-slide-deck) <br>
- [Project homepage](https://github.com/JimLiu/baoyu-skills#baoyu-slide-deck) <br>
- [Codex image generation wrapper](references/codex-imagegen.md) <br>
- [Presentation analysis framework](references/analysis-framework.md) <br>
- [Outline template](references/outline-template.md) <br>
- [Base prompt](references/base-prompt.md) <br>
- [Layout gallery](references/layouts.md) <br>
- [Design guidelines](references/design-guidelines.md) <br>
- [Content and style rules](references/content-rules.md) <br>
- [Slide modification guide](references/modification-guide.md) <br>
- [Preferences schema](references/config/preferences-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown instructions with generated outline and prompt files, raster slide images, and optional PPTX/PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses prompt files as reproducibility records; merge scripts require bun or npx.] <br>

## Skill Version(s): <br>
1.117.4 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
