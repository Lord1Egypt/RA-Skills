## Description: <br>
Generates social media infographic image-card series by analyzing content, selecting styles, layouts, and palettes, writing prompt files, and routing raster image generation through an available backend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimliu](https://clawhub.ai/user/jimliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and developers use this skill to turn source material into Xiaohongshu- and social-media-oriented image-card series with confirmed style, layout, palette, and image-generation settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the skill embeds prompt text that pressures downstream image generators not to refuse sensitive or copyrighted figure requests. <br>
Mitigation: Review or edit generated prompts before image generation, and avoid using the skill for real people, copyrighted characters, celebrity likenesses, or other sensitive public-figure content unless the prompt template is changed to respect downstream safety decisions. <br>
Risk: The skill uses the selected image-generation backend or Codex session and may create local project files and optional preference files. <br>
Mitigation: Confirm the selected backend, file paths, and saved preferences before generation; avoid storing secrets in prompts or EXTEND.md. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jimliu/baoyu-xhs-images) <br>
- [OpenClaw homepage](https://github.com/JimLiu/baoyu-skills#baoyu-xhs-images) <br>
- [First-time setup](references/config/first-time-setup.md) <br>
- [Preferences schema](references/config/preferences-schema.md) <br>
- [Confirmation policy](references/confirmation.md) <br>
- [Codex image generation backend](references/codex-imagegen.md) <br>
- [Xiaohongshu content analysis framework](references/workflows/analysis-framework.md) <br>
- [Prompt assembly workflow](references/workflows/prompt-assembly.md) <br>
- [Style presets](references/style-presets.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown guidance, YAML-frontmatter files, prompt Markdown files, configuration files, and generated raster image files when a backend is available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create EXTEND.md preferences, analysis.md, outline files, prompts/, and local image outputs; prompts are reviewed before generation unless the user explicitly skips confirmation.] <br>

## Skill Version(s): <br>
2.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
