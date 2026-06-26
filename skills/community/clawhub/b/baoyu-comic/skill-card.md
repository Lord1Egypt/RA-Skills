## Description: <br>
Knowledge comic creator supporting multiple art styles and tones. Creates original educational comics with detailed panel layouts and batch-capable image generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimliu](https://clawhub.ai/user/jimliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, educators, and creators use this skill to turn source material into original educational comics, including analysis, storyboards, character guides, image prompts, generated pages, and a final PDF. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Preference files can persist watermark text and other defaults across projects. <br>
Mitigation: Review the first-time setup and choose project-local preferences when settings should not be reused. <br>
Risk: Watermark and preference fields could contain secrets or sensitive text. <br>
Mitigation: Avoid placing secrets, private identifiers, or sensitive content in watermark or preference fields. <br>
Risk: Image generation may invoke installed backends or the Codex CLI using the user's existing local login. <br>
Mitigation: Confirm the selected image backend and account context before generating images. <br>
Risk: The ohmsha preset defaults to recognizable Doraemon characters, which may be unsuitable for original or rights-sensitive work. <br>
Mitigation: Use custom characters when original or rights-safe output is required. <br>


## Reference(s): <br>
- [Baoyu Comic Homepage](https://github.com/JimLiu/baoyu-skills#baoyu-comic) <br>
- [Complete Workflow](references/workflow.md) <br>
- [Analysis Framework](references/analysis-framework.md) <br>
- [Auto Selection](references/auto-selection.md) <br>
- [Partial Workflows](references/partial-workflows.md) <br>
- [Codex Image Generation](references/codex-imagegen.md) <br>
- [First-Time Setup](references/config/first-time-setup.md) <br>
- [Preferences Schema](references/config/preferences-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown workflow artifacts, saved image prompts, generated image files, and an optional PDF] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses project or user preferences, supports batch image generation, and may use bun or npx for PDF merging.] <br>

## Skill Version(s): <br>
1.117.4 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
