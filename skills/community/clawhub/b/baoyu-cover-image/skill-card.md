## Description:

Generates article cover images with configurable type, palette, rendering, text, mood, aspect ratio, and image-generation backend options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimliu](https://clawhub.ai/user/jimliu)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, developers, and content teams use this skill to turn article content or cover-image requests into reproducible prompts and raster cover images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill can weaken safety refusals.

Mitigation: Review generated prompts and remove or revise anti-refusal language before using the skill in environments with strict content-safety requirements.

Risk: Fallback paths can run unverified local or downloaded tooling.

Mitigation: Prefer a native trusted image-generation backend, avoid the direct codex-imagegen fallback unless the wrapper path is trusted, do not set BAOYU_CODEX_IMAGEGEN_BIN to arbitrary files, and avoid the unpinned npx -y bun path.

Risk: Automatic design choices can proceed without user confirmation when confirmation is disabled.

Mitigation: Keep confirmation enabled unless the user is comfortable with automatic choices.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jimliu/skills/baoyu-cover-image)
- [Project Homepage](https://github.com/JimLiu/baoyu-skills#baoyu-cover-image)
- [Auto-Selection Rules](references/auto-selection.md)
- [Type Composition Guidelines](references/types.md)
- [Style Presets](references/style-presets.md)
- [Compatibility Matrices](references/compatibility.md)
- [Prompt Template](references/workflow/prompt-template.md)
- [Reference Image Handling](references/workflow/reference-images.md)
- [Codex Imagegen Wrapper Invocation](references/codex-imagegen.md)
- [Preferences Schema](references/config/preferences-schema.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with prompt files, shell commands, and raster image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes reproducibility prompts before image generation and reports the generated cover image location.]

## Skill Version(s):

1.117.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
