## Description: <br>
Generates article cover images with configurable type, palette, rendering, text, mood, font, and aspect-ratio settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimliu](https://clawhub.ai/user/jimliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content creators use this skill to turn article content or prompts into reproducible raster cover-image prompts and generated image files with configurable visual style dimensions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image-safety language may encourage continued generation around sensitive or copyrighted subject refusals. <br>
Mitigation: Use only rights-cleared subjects, keep platform safety policy higher priority than skill guidance, and review prompts before generation. <br>
Risk: The skill can create prompt, source, reference, configuration, and output image files, including cross-project defaults if user-level preferences are used. <br>
Mitigation: Prefer project-local preferences for managed releases and review configured output directories before generation. <br>
Risk: Image generation may invoke runtime-native or external backends that depend on local credentials or subscriptions. <br>
Mitigation: Confirm backend selection, avoid placing secrets in prompts or logs, and use only approved image-generation backends. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jimliu/baoyu-cover-image) <br>
- [Project Homepage](https://github.com/JimLiu/baoyu-skills#baoyu-cover-image) <br>
- [Auto-Selection Rules](references/auto-selection.md) <br>
- [Base Prompt](references/base-prompt.md) <br>
- [Codex Image Generation Wrapper](references/codex-imagegen.md) <br>
- [Compatibility Matrices](references/compatibility.md) <br>
- [Style Presets](references/style-presets.md) <br>
- [Type Composition Guidelines](references/types.md) <br>
- [Visual Elements Library](references/visual-elements.md) <br>
- [Confirmation Workflow](references/workflow/confirm-options.md) <br>
- [Prompt Template](references/workflow/prompt-template.md) <br>
- [Reference Image Workflow](references/workflow/reference-images.md) <br>
- [Preferences Schema](references/config/preferences-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown prompts and user-facing guidance, with optional shell command invocations and generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a reproducibility prompt before generation and may create source, reference, configuration, and cover image files under the configured output location.] <br>

## Skill Version(s): <br>
1.117.5 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
