## Description: <br>
Generates infographic image card series with 12 visual styles, 8 layouts, and 3 color palettes for social media posts and visual summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimliu](https://clawhub.ai/user/jimliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content creators use this skill to turn source content into multi-card infographic image series for Xiaohongshu, WeChat, and similar social media channels. It guides style, layout, palette, outline, prompt preparation, and image generation workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt-safety language may encourage stylized substitutes for sensitive or copyrighted figure requests instead of normal refusal or policy handling. <br>
Mitigation: Review or revise the prompt-safety language before installation, and require the selected image backend's policy handling for sensitive or copyrighted subject requests. <br>
Risk: The workflow writes source summaries, outlines, prompts, preferences, and generated assets to local files. <br>
Mitigation: Use an appropriate project workspace, review saved prompt and preference files before sharing, and avoid placing sensitive source content in generated prompt records. <br>


## Reference(s): <br>
- [Baoyu Image Cards homepage](https://github.com/JimLiu/baoyu-skills#baoyu-image-cards) <br>
- [Confirmation questions](references/confirmation.md) <br>
- [Style presets](references/style-presets.md) <br>
- [Canvas and layout guidance](references/elements/canvas.md) <br>
- [Prompt assembly workflow](references/workflows/prompt-assembly.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions, prompt files, outline files, preference configuration, and generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a raster image generation backend and writes prompts before invoking image generation.] <br>

## Skill Version(s): <br>
1.117.2 (source: server release metadata and changelog dated 2026-05-17) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
